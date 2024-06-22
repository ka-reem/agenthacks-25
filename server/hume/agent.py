import json
import re
from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain.agents import load_tools, AgentExecutor, create_json_chat_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import inflect
from fastapi import WebSocket, APIRouter

router = APIRouter(prefix="/hume")

@router.websocket("/")
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

class Agent:
    def __init__(self, *, system_prompt: str):
        self.system_prompt = system_prompt
        
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0.8,
            max_tokens=1024,
            timeout=None,
            max_retries=2,
        )
        
    def add_prosody_to_utterance(self, utterance: str, prosody: dict) -> str:
        prosody_string = ", ".join(prosody.keys())
        return f"Speech: {utterance} {prosody_string}"
    
    
    async def get_responses(self, message: str, chat_history=None) -> list[str]:
        if chat_history is None:
            chat_history = []
            
        human = HumanMessage(content=message)
        chat_history.append(human)

        response = self.llm.astream(
            chat_history
        )
        async for chunk in response:
            output = chunk.content
            numbers = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b", output)
            
            for number in numbers:
                words = self.number_to_words(number)
                output = output.replace(number, words, 1)

            yield json.dumps({"type": "assistant_input", "text": output})
        
        yield json.dumps({"type": "assistant_end"})
    
    def parse_hume_message(self, messages_payload: dict) -> [str, list[any]]:
        messages = messages_payload["messages"]
        last_user_message = messages[-1]["message"]["content"]

        chat_history = [SystemMessage(content=self.system_prompt)]

        # Iterate through each message in the data except the last one
        for message in messages[:-1]:

            # Extract the message role and content
            message_object = message["message"]

            # Extract the prosody model scores, if available
            prosody_scores = message.get("models", {}).get("prosody", {}).get("scores", {})

            # Sort the prosody scores based on score, in descending order
            sorted_entries = sorted(
                prosody_scores.items(), key=lambda x: x[1], reverse=True
            )

            # Extract the top 3 entries
            top_entries = sorted_entries[:3]

            # Format the top entries as a dictionary for easier readability
            top_entries_dict = {entry[0]: entry[1] for entry in top_entries}
            
            contextualized_utterance = self.add_prosody_to_utterance(
                message_object["content"], top_entries_dict
            )

            if message_object["role"] == "user":
                chat_history.append(HumanMessage(content=contextualized_utterance))
            elif message_object["role"] == "assistant":
                chat_history.append(AIMessage(content=contextualized_utterance))

        return [last_user_message, chat_history]

    def generate_response(self, *, prompt: str):
        pass
    
    def number_to_words(self, number):
        p = inflect.engine()
        words = p.number_to_words(number)
        return words