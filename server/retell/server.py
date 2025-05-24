import json
import os
import asyncio
from dotenv import load_dotenv
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, PlainTextResponse
from concurrent.futures import TimeoutError as ConnectionTimeoutError
from twilio.twiml.voice_response import VoiceResponse
from retell import Retell
from retell.resources.call import RegisterCallResponse
from .custom_types import (
    ConfigResponse,
    ResponseRequiredRequest,
)
from .twilio_server import TwilioClient
from .llm import LlmClient  # or use .llm_with_func_calling
import uuid
from datetime import datetime
from server.db import update_call, get_call, get_all_calls
from server.socket_manager import manager
from server.evals import eval, hume_eval
from server.geocoding import geocode, street_view

print(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(override=True, dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
retell = Retell(api_key=os.environ["RETELL_API_KEY"])

# Custom Twilio if you want to use your own Twilio API Key
twilio_client = TwilioClient()

router = APIRouter(
    prefix="/retell",
    tags=["retell"],
    responses={404: {"description": "Not found"}},
)


# Handle webhook from Retell server. This is used to receive events from Retell server.
# Including call_started, call_ended, call_analyzed
@router.post("/webhook")
async def handle_webhook(request: Request):
    try:
        post_data = await request.json()
        valid_signature = retell.verify(
            json.dumps(post_data, separators=(",", ":")),
            api_key=str(os.environ["RETELL_API_KEY"]),
            signature=str(request.headers.get("X-Retell-Signature")),
        )
        if not valid_signature:
            print(
                "Received Unauthorized",
                post_data["event"],
                post_data["data"]["call_id"],
            )
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        if post_data["event"] == "call_started":
            print("Call started event", post_data["data"]["call_id"])
        elif post_data["event"] == "call_ended":
            print("Call ended event", post_data["data"]["call_id"])
        elif post_data["event"] == "call_analyzed":
            print("Call analyzed event", post_data["data"]["call_id"])
        else:
            print("Unknown event", post_data["event"])
        return JSONResponse(status_code=200, content={"received": True})
    except Exception as err:
        print(f"Error in webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )


# Twilio voice webhook. This will be called whenever there is an incoming or outgoing call.
# Register call with Retell at this stage and pass in returned call_id to Retell.
@router.post("/twilio-voice-webhook/{agent_id_path}")
async def handle_twilio_voice_webhook(request: Request, agent_id_path: str):
    try:
        # Check if it is machine
        post_data = await request.form()
        if "AnsweredBy" in post_data and post_data["AnsweredBy"] == "machine_start":
            twilio_client.end_call(post_data["CallSid"])
            return PlainTextResponse("")
        elif "AnsweredBy" in post_data:
            return PlainTextResponse("")

        call_response: RegisterCallResponse = retell.call.register(
            agent_id=agent_id_path,
            audio_websocket_protocol="twilio",
            audio_encoding="mulaw",
            sample_rate=8000,  # Sample rate has to be 8000 for Twilio
            from_number=post_data["From"],
            to_number=post_data["To"],
            metadata={
                "twilio_call_sid": post_data["CallSid"],
            },
        )
        print(f"Call response: {call_response}")

        response = VoiceResponse()
        start = response.connect()
        start.stream(
            url=f"wss://api.retellai.com/audio-websocket/{call_response.call_id}"
        )
        return PlainTextResponse(str(response), media_type="text/xml")
    except Exception as err:
        print(f"Error in twilio voice webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )


# Only used for web call frontend to register call so that frontend don't need api key.
# If you are using Retell through phone call, you don't need this API. Because
# this.twilioClient.ListenTwilioVoiceWebhook() will include register-call in its function.
@router.post("/register-call-on-your-server")
async def handle_register_call(request: Request):
    try:
        post_data = await request.json()
        call_response = retell.call.register(
            agent_id=post_data["agent_id"],
            audio_websocket_protocol="web",
            audio_encoding="s16le",
            sample_rate=post_data[
                "sample_rate"
            ],  # Sample rate has to be 8000 for Twilio
        )
        print(f"Call response: {call_response}")
    except Exception as err:
        print(f"Error in register call: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )


# Start a websocket server to exchange text input and output with Retell server. Retell server
# will send over transcriptions and other information. This server here will be responsible for
# generating responses with LLM and send back to Retell server.
@router.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    try:
        await websocket.accept()
        llm_client = LlmClient()

        # Send optional config to Retell server
        config = ConfigResponse(
            response_type="config",
            config={
                "auto_reconnect": True,
                "call_details": True,
            },
            response_id=1,
        )
        await websocket.send_json(config.__dict__)

        # Send first message to signal ready of server
        response_id = 0
        first_event = llm_client.draft_begin_message()
        await websocket.send_json(first_event.__dict__)
        twilio_sid = None

        async def handle_message(request_json):
            nonlocal twilio_sid
            nonlocal response_id

            # There are 5 types of interaction_type: call_details, pingpong, update_only, response_required, and reminder_required.
            # Not all of them need to be handled, only response_required and reminder_required.
            if request_json["interaction_type"] == "call_details":
                print(json.dumps(request_json, indent=2))
                twilio_sid = request_json["call"]["metadata"]["twilio_call_sid"]
                return
            if request_json["interaction_type"] == "ping_pong":
                await websocket.send_json(
                    {
                        "response_type": "ping_pong",
                        "timestamp": request_json["timestamp"],
                    }
                )
                return
            if request_json["interaction_type"] == "update_only":
                return
            if (
                request_json["interaction_type"] == "response_required"
                or request_json["interaction_type"] == "reminder_required"
            ):
                response_id = request_json["response_id"]
                request = ResponseRequiredRequest(
                    interaction_type=request_json["interaction_type"],
                    response_id=response_id,
                    transcript=request_json["transcript"],
                )
                print(
                    f"""Received interaction_type={request_json['interaction_type']}, response_id={response_id}, last_transcript={request_json['transcript'][-1]['content']}"""
                )

                response_completed = True
                async for event in llm_client.draft_response(request):
                    await websocket.send_json(event.__dict__)
                    if request.response_id < response_id:
                        response_completed = False
                        break  # new response needed, abandon this one

                if response_completed:
                    # Update call data in database
                    updated_data = {
                        "id": twilio_sid,
                        "mode": "retell",
                        "time": datetime.now().isoformat(),
                        "transcript": request_json["transcript"],
                    }
                    update_call(twilio_sid, updated_data)

                    # Broadcast updated calls to all connected clients
                    all_calls = get_all_calls()
                    await manager.broadcast(
                        {
                            "event": "db_response",
                            "data": all_calls,
                        }
                    )

                    # Perform additional evaluations
                    current_data = str(get_call(twilio_sid))
                    hume_task = hume_eval(request_json["transcript"][-1]["content"])
                    eval_task = eval(
                        request_json["transcript"][-1]["content"], current_data
                    )
                    results = await asyncio.gather(hume_task, eval_task)

                    updated_data = {
                        "emotions": results[0],
                        **json.loads(results[1]),
                    }

                    if updated_data.get("location_name"):
                        res = geocode(updated_data["location_name"])
                        updated_data["location_coords"] = res[0]["geometry"]["location"]
                        updated_data["street_view"] = street_view(
                            updated_data["location_coords"]["lat"],
                            updated_data["location_coords"]["lng"],
                        )

                    update_call(twilio_sid, updated_data)
                    all_calls = get_all_calls()
                    await manager.broadcast(
                        {
                            "event": "db_response",
                            "data": all_calls,
                        }
                    )

        async for data in websocket.iter_json():
            asyncio.create_task(handle_message(data))

    except WebSocketDisconnect:
        print(f"LLM WebSocket disconnected for {call_id}")
    except ConnectionTimeoutError as e:
        print(f"Connection timeout error for {call_id}")
    except Exception as e:
        print(f"Error in LLM WebSocket: {e} for {call_id}")
        await websocket.close(1011, "Server error")
    finally:
        print(f"LLM WebSocket connection closed for {call_id}")
