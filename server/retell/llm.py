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
from server.prompts import SYSTEM_PROMPT


class LlmClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            # organization=os.environ["OPENAI_ORGANIZATION_ID"],
            api_key=os.environ["OPENAI_API_KEY"],
        )
        # self.mistral = ChatMistralAI(api_key=os.environ["MISTRAL_API_KEY"])

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
                "content": SYSTEM_PROMPT,
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
        stream = await self.client.chat.completions.create(
            model="gpt-4o",  # Or use a 3.5 model for speed
            messages=prompt,
            stream=True,
        )
        # async for chunk in self.mistral.astream(input=prompt):
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response = ResponseResponse(
                    response_id=request.response_id,
                    content=chunk.choices[0].delta.content,
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
