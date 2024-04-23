from typing import Optional

import httpx
from pydantic import BaseModel


class EmojiExplainResponse(BaseModel):
    """
    This response contains either the explanation of the emoji or an error message in case the emoji is not supported.
    """

    meaning: str
    error: Optional[str] = None


async def explainEmoji(emoji_character: str) -> EmojiExplainResponse:
    """
    This POST endpoint receives an emoji as input from the user, sends a request to the GROQ platform to retrieve the explanation and meaning of the provided emoji. The endpoint integrates with the GROQ API, crafting a query based on the received emoji and parsing the GROQ response to format a user-friendly explanation. Expected responses include a success case with the emoji's meaning or a fail case with an error message (e.g., unsupported emoji). This route is essential to allow real-time emoji explanations to users across various devices, owing to the Responsive Design Module's capability to adapt the response format according to the device.

    Args:
        emoji_character (str): The emoji character for which the meaning is requested.

    Returns:
        EmojiExplainResponse: This response contains either the explanation of the emoji or an error message in case the emoji is not supported.

    Example:
        response = explainEmoji('😀')
        response.meaning
        > 'A yellow face with simple, open eyes and a broad, open smile.'
    """
    emoji_api_url = "https://console.groq.com/api/emoji"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(emoji_api_url, json={"emoji": emoji_character})
            response.raise_for_status()
            data = response.json()
            if "meaning" in data:
                return EmojiExplainResponse(meaning=data["meaning"])
            else:
                return EmojiExplainResponse(
                    meaning="", error="Meaning not found for the provided emoji."
                )
        except httpx.HTTPStatusError:
            return EmojiExplainResponse(
                meaning="", error="Invalid response from the server."
            )
        except httpx.RequestError:
            return EmojiExplainResponse(
                meaning="", error="Failed to connect to the GROQ server."
            )
        except Exception as e:
            return EmojiExplainResponse(meaning="", error=str(e))
