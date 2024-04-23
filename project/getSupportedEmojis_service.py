from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GETSupportedEmojisRequest(BaseModel):
    """
    This request model captures any header or parameters required to validate or format the data retrieval, such as content-type or locale. However, given the outlined functionality, it is expected to be quite straightforward without a need for path or query parameters.
    """

    pass


class Emoji(BaseModel):
    """
    An object representing an emoji, including its unique character and associated meaning.
    """

    character: str
    meaning: str


class GETSupportedEmojisResponse(BaseModel):
    """
    The response model outputs a list of supported emojis. Each emoji in the list contains key characteristics like the symbol itself and its meaning.
    """

    emojis: List[Emoji]


async def getSupportedEmojis(
    request: GETSupportedEmojisRequest,
) -> GETSupportedEmojisResponse:
    """
    This GET endpoint provides a list of all emojis that can be interpreted by the system. It queries an internal database through the API Communication Module to retrieve the supported emoji list, ensuring that it is always up-to-date. This endpoint is primarily informational and is used to enhance user experience by informing them of the supported functionalities.

    Args:
        request (GETSupportedEmojisRequest): This request model captures any header or parameters required to validate or format the data retrieval, such as content-type or locale. However, given the outlined functionality, it is expected to be quite straightforward without a need for path or query parameters.

    Returns:
        GETSupportedEmojisResponse: The response model outputs a list of supported emojis. Each emoji in the list contains key characteristics like the symbol itself and its meaning.
    """
    emojis_data = await prisma.models.Emoji.prisma().find_many()
    emojis_list = [
        Emoji(character=emoji.character, meaning=emoji.meaning) for emoji in emojis_data
    ]
    return GETSupportedEmojisResponse(emojis=emojis_list)
