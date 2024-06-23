import dotenv

dotenv.load_dotenv()
from openai import AsyncOpenAI

import os
import websockets
import json

websocket_url = f"wss://api.hume.ai/v0/stream/models"

HUME_API_KEY = os.getenv("HUME_API_KEY")


async def eval(message: str, current_data: str):
    client = AsyncOpenAI()
    system_message = """
    You are an ai system to evaluate 911 transcripts. You should analyze the calls for their severity, type, name, type, title, summary, and location
    Follow these rules:
        If not enough information is provided, set values to empty strings.
        If no new information is provided, return the current data.
        If the severity is DISPATCHED, do not change the severity.
        Always have a title, even if its "Not enough information provided"
        The audio transcription is sometimes not perfect, try to make your best guess.
        
    Output a json in the following format:
    {
        "recommendation": str,
        "severity": "MODERATE" | "CRITICAL",
        "type": "Fire" | "Hospital" | "Police",
        "name": str,
        "title": str,
        "summary": str,
        "location_name": str (valid address nearby San Francisco Bay Area)
    }
    """

    evals = await client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": message + "\n\nCurrent Data:\n\n" + current_data,
            },
        ],
    )
    return evals.choices[0].message.content


interesting_emotions = [
    "anger",
    "anxiety",
    "calmness",
    "concentration",
    "confusion",
    "distress",
    "fear",
    "horror",
    "pain",
    "sadness",
]


async def hume_eval(message: str):
    async with websockets.connect(
        websocket_url, extra_headers={"X-Hume-Api-Key": HUME_API_KEY}
    ) as websocket:
        await websocket.send(
            json.dumps({"data": message, "models": {"language": {}}, "raw_text": True})
        )
        data = await websocket.recv()
        response_data = json.loads(data)
        emotions_data = response_data.get("language", {}).get("predictions", [])
        emotion_scores = {}
        total_words = len(emotions_data)

        for word_data in emotions_data:
            word_emotions = word_data.get("emotions", [])
            for emotion in word_emotions:
                if emotion["name"].lower() in interesting_emotions:
                    if emotion["name"] in emotion_scores:
                        emotion_scores[emotion["name"]] += emotion["score"]
                    else:
                        emotion_scores[emotion["name"]] = emotion["score"]

        # Calculating average scores
        for emotion in emotion_scores:
            emotion_scores[emotion] /= total_words

        # Sorting and selecting the top three emotions for the entire text chunk
        top_three_overall_emotions = sorted(
            emotion_scores.items(), key=lambda item: item[1], reverse=True
        )[:3]

        # Format the result according to the specified structure
        formatted_result = [
            {"emotion": emotion, "intensity": score}
            for emotion, score in top_three_overall_emotions
        ]

        return formatted_result
