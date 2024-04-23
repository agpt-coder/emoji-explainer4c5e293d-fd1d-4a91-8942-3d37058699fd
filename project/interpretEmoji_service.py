import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class EmojiInterpretationResponse(BaseModel):
    """
    Response model representing the interpreted meaning of the provided emoji character.
    """

    meaning: str


async def interpretEmoji(emoji: str) -> EmojiInterpretationResponse:
    """
    This endpoint receives a JSON payload containing an emoji character and sends a request to the Groq API to fetch the interpretation of the emoji. It processes the emoji input, forwards it to the Groq service, and parses the response to provide a meaningful interpretation. The endpoint expects a payload of {'emoji': 'emoji_character'} and returns a JSON object {'meaning': 'explanation_text'}. This service is crucial for delivering the core functionality of the emoji-explainer product.

    Args:
    emoji (str): A single emoji character for which the meaning is requested.

    Returns:
    EmojiInterpretationResponse: Response model representing the interpreted meaning of the provided emoji character.
    """
    async with httpx.AsyncClient() as client:
        url = "https://console.groq.com/api/interpret"
        headers = {"Content-Type": "application/json"}
        body = {"emoji": emoji}
        response = await client.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json()
            meaning = data.get("meaning", "No interpretation found.")
            try:
                emoji_entry = await prisma.models.Emoji.prisma().create(
                    data={"character": emoji, "meaning": meaning}
                )
            except Exception as e:
                emoji_entry = await prisma.models.Emoji.prisma().find_unique(
                    where={"character": emoji}
                )
                meaning = emoji_entry.meaning if emoji_entry else meaning
            return EmojiInterpretationResponse(meaning=meaning)
        else:
            return EmojiInterpretationResponse(meaning="Failed to interpret the emoji.")
