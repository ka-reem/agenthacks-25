import json
import re
from langchain_anthropic import ChatAnthropic
from langchain import hub
from langchain.agents import load_tools, AgentExecutor, create_json_chat_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import inflect


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