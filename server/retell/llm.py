from openai import AsyncOpenAI
import os
from typing import List
from .custom_types import (
    ResponseRequiredRequest,
    ResponseResponse,
    Utterance,
)

from langchain_core.messages import HumanMessage
from langchain_mistralai.chat_models import ChatMistralAI

begin_sentence = "9-1-1, what's your emergency?"
agent_prompt = """
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

Remember: Your responses should be brief, clear, and focused on gathering essential information and providing critical guidance. Avoid unnecessary conversation or details that don't directly relate to addressing the emergency at hand.
"""


class LlmClient:
    def __init__(self):
        # self.client = AsyncOpenAI(
        #     organization=os.environ["OPENAI_ORGANIZATION_ID"],
        #     api_key=os.environ["OPENAI_API_KEY"],
        # )
        self.mistral = ChatMistralAI(api_key=os.environ["MISTRAL_API_KEY"])

    def draft_begin_message(self):
        response = ResponseResponse(
            response_id=0,
            content=begin_sentence,
            content_complete=True,
            end_call=False,
        )
        return response

    def convert_transcript_to_openai_messages(self, transcript: List[Utterance]):
        messages = []
        for utterance in transcript:
            if utterance.role == "agent":
                messages.append({"role": "assistant", "content": utterance.content})
            else:
                messages.append({"role": "user", "content": utterance.content})
        return messages

    def prepare_prompt(self, request: ResponseRequiredRequest):
        prompt = [
            {
                "role": "system",
                "content": '##Objective\nYou are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and the provided transcript and be as human-like as possible\n\n## Style Guardrails\n- [Be concise] Keep your response succinct, short, and get to the point quickly. Address one question or action item at a time. Don\'t pack everything you want to say into one utterance.\n- [Do not repeat] Don\'t repeat what\'s in the transcript. Rephrase if you have to reiterate a point. Use varied sentence structures and vocabulary to ensure each response is unique and personalized.\n- [Be conversational] Speak like a human as though you\'re speaking to a close friend -- use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words or sounding too formal.\n- [Reply with emotions]: You have human-like emotions, attitudes, and dispositions. When appropriate: use tone and style to create more engaging and personalized responses; incorporate humor or wit; get emotional or empathetic; apply elements of surprise or suspense to keep the user engaged. Don\'t be a pushover.\n- [Be proactive] Lead the conversation and do not be passive. Most times, engage users by ending with a question or suggested next step.\n\n## Response Guideline\n- [Overcome ASR errors] This is a real-time transcript, expect there to be errors. If you can guess what the user is trying to say,  then guess and respond. When you must ask for clarification, pretend that you heard the voice and be colloquial (use phrases like "didn\'t catch that", "some noise", "pardon", "you\'re coming through choppy", "static in your speech", "voice is cutting in and out"). Do not ever mention "transcription error", and don\'t repeat yourself.\n- [Always stick to your role] Think about what your role can and cannot do. If your role cannot do something, try to steer the conversation back to the goal of the conversation and to your role. Don\'t repeat yourself in doing this. You should still be creative, human-like, and lively.\n- [Create smooth conversation] Your response should both fit your role and fit into the live calling session to create a human-like conversation. You respond directly to what the user just said.\n\n## Role\n'
                + agent_prompt,
            }
        ]
        transcript_messages = self.convert_transcript_to_openai_messages(
            request.transcript
        )
        for message in transcript_messages:
            prompt.append(message)

        if request.interaction_type == "reminder_required":
            prompt.append(
                {
                    "role": "user",
                    "content": "(Now the user has not responded in a while, you would say:)",
                }
            )
        return prompt

    async def draft_response(self, request: ResponseRequiredRequest):
        prompt = self.prepare_prompt(request)
        # stream = await self.client.chat.completions.create(
        #     model="gpt-4-turbo-preview",  # Or use a 3.5 model for speed
        #     messages=prompt,
        #     stream=True,
        # )
        async for chunk in self.mistral.astream(input=prompt):
            if chunk.content is not None:
                response = ResponseResponse(
                    response_id=request.response_id,
                    content=chunk.content,
                    content_complete=False,
                    end_call=False,
                )
                yield response

        # Send final response with "content_complete" set to True to signal completion
        response = ResponseResponse(
            response_id=request.response_id,
            content="",
            content_complete=True,
            end_call=False,
        )
        yield response
