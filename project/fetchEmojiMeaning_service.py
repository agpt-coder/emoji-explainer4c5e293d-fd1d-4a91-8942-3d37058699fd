import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class EmojiExplainerResponse(BaseModel):
    """
    The response model that represents the explanation of the emoji obtained from the GROQ API. It encapsulates both the character and its meaning.
    """

    emoji: str
    explanation: str


async def fetchEmojiMeaning(emoji: str) -> EmojiExplainerResponse:
    """
    This endpoint allows users to input an emoji and request its meaning from the GROQ API. The route expects an emoji character as input, sends a query to the GROQ API, and returns the explanation of the emoji. It's essential to handle errors gracefully, such as invalid emoji inputs or issues with GROQ API communication.

    Args:
        emoji (str): The emoji character for which the explanation is requested.

    Returns:
        EmojiExplainerResponse: The response model that represents the explanation of the emoji obtained from the GROQ API. It encapsulates both the character and its meaning.
    """
    stored_emoji = await prisma.models.Emoji.prisma().find_unique(
        where={"character": emoji}
    )
    if stored_emoji:
        return EmojiExplainerResponse(emoji=emoji, explanation=stored_emoji.meaning)
    api_url = f"https://api.groq.com/emoji?char={emoji}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()
            result_data = response.json()
            meaning = result_data["explanation"]
            new_emoji = await prisma.models.Emoji.prisma().create(
                data={"character": emoji, "meaning": meaning}
            )
            return EmojiExplainerResponse(emoji=emoji, explanation=new_emoji.meaning)
        except httpx.HTTPStatusError as e:
            raise ValueError(
                f"HTTP Error occurred: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise ValueError(f"Network Error: {e.request.url} - {str(e)}")
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")
