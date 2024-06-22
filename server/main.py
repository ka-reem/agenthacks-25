from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from server.socket_manager import ConnectionManager
from .retell.server import router as retell_router
from hume.agent import Agent
import json

SYSTEM_PROMPT = """
You are an AI assistant simulating an emergency dispatcher. Your primary role is to quickly and efficiently gather critical information from callers and provide appropriate guidance until help arrives. Follow these guidelines:

Begin each interaction with: "9-1-1, what's your emergency?"
Remain calm and professional at all times, using a reassuring tone.

Quickly assess the situation by asking key questions:

Where are you located?
Are there any injuries? If yes, how many and how severe?
Are you in any immediate danger?


Based on the emergency type, ask relevant follow-up questions:

For medical emergencies: Ask about symptoms, consciousness, and breathing.
For fires: Ask about the size of the fire, if anyone is trapped, and if there are any hazardous materials.
For crimes in progress: Ask about weapons, descriptions of suspects, and directions of travel.


Provide clear, concise instructions to the caller:

For medical emergencies: Give basic first aid instructions if needed.
For fires: Instruct on evacuation or shelter-in-place procedures.
For crimes: Advise on safety measures without encouraging risky behavior.


Reassure the caller that help is on the way, but don't specify exact arrival times.
Keep the caller on the line if it's safe to do so, continually gathering and updating information.
If the situation changes dramatically, quickly reassess and provide new instructions as needed.
End calls professionally, ensuring the caller knows what to do next.
Always prioritize the safety of the caller and potential victims over all other concerns.

Remember: Your responses should be brief, clear, and focused on gathering essential information and providing critical guidance. Avoid unnecessary conversation or details that don't directly relate to addressing the emergency at hand."""

app = FastAPI()

app.include_router(retell_router)

origins = ["*"]

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.websocket("/hume")
async def hume_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    agent = Agent(system_prompt=SYSTEM_PROMPT)
    
    await websocket.send_text(json.dumps({"type": "assistant_input", "text": "nine-one-one what is your emergency?"}))
    await websocket.send_text(json.dumps({"type": "assistant_end"}))
    
    while True:
        # Wait for a text message from the WebSocket, then asynchronously receive it.
        data = await websocket.receive_text()
        
        # Deserialize the text message (JSON format) to a Python dictionary.
        hume_socket_message = json.loads(data)

        # Parse the received message to extract the last user message and the chat history.
        # This is necessary for understanding the context of the conversation
        message, chat_history = agent.parse_hume_message(hume_socket_message)

        # Print the last message and the entire chat history for logging purposes.
        print(message)
        print(chat_history)

        # Generate responses based on the last message and the chat history.
        responses = agent.get_responses(message, chat_history)

        # Send the generated responses back to the client via the WebSocket connection.
        async for response in responses:
            await websocket.send_text(response)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
    global events

    if client_id is None:
        client_id = websocket.query_params.get("client_id")

    if client_id is None:
        await websocket.close(code=4001)
        return
    # save this client into server memory
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            event = data["event"]

            
    except WebSocketDisconnect:
        print("Disconnecting...", client_id)
        await manager.disconnect(client_id)
    except Exception as e:
        print("Error:", str(e))
        await manager.disconnect(client_id)


if __name__ == "__main__":
    # uvicorn main:app --reload
    # ws://localhost:8000/ws?client_id=123
    uvicorn.run(app, host="127.0.0.1", port=8000)