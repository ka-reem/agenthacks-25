from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from server.socket_manager import manager
from server.retell.server import router as retell_router
from server.hume.agent import router as hume_router

# Import the necessary function from the db module
from server.db import get_all_calls

app = FastAPI()

app.include_router(retell_router)
app.include_router(hume_router)

origins = ["*"]


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: Optional[str] = None):
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
            print(event)
            if event == "get_db":
                # Retrieve all calls from the database
                all_calls = get_all_calls()
                message = {
                    "event": "db_response",
                    "data": all_calls,
                }
                # Send the calls data back to the client
                await manager.send_personal_message(
                    message,
                    websocket,
                )

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
