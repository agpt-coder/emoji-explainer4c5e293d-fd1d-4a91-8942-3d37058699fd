from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class HistoryRequest(BaseModel):
    """
    This model represents the request for fetching the history of emoji interpretations. It requires no explicit fields as the user identity and permissions will be handled by the authentication middleware.
    """

    pass


class EmojiDetails(BaseModel):
    """
    Structure containing details of an emoji interpretation.
    """

    emoji: str
    meaning: str


class HistoryResponse(BaseModel):
    """
    This model represents the response for the history of emojis interpreted by the user. It returns a list of emoji details including the character and its meaning.
    """

    recent_emojis: List[EmojiDetails]


async def getHistory(request: HistoryRequest) -> HistoryResponse:
    """
    Fetches a list of recently interpreted emojis along with their meanings from the database. This endpoint provides history tracking and retrieval functionality, enhancing user experience by allowing them to view past interpretations. It returns a JSON array of recent interpretations, e.g., [{'emoji': 'emoji_character', 'meaning': 'interpretation_text'}]. This service is intended for use by logged-in users to view their personal emoji interpretation history.

    Args:
        request (HistoryRequest): This model represents the request for fetching the history of emoji interpretations. It requires no explicit fields as the user identity and permissions will be handled by the authentication middleware.

    Returns:
        HistoryResponse: This model represents the response for the history of emojis interpreted by the user. It returns a list of emoji details including the character and its meaning.

    Example:
        request = HistoryRequest()
        response = await getHistory(request)
        response.recent_emojis
        > [{'emoji': '😀', 'meaning': 'grinning face'}, ...]
    """
    user_id = 1
    feedbacks = await prisma.models.Feedback.prisma().find_many(
        where={"userId": user_id},
        include={"emoji": True},
        order=[{"createdAt": "desc"}],
    )
    recent_emojis = [
        EmojiDetails(emoji=f.emoji.character, meaning=f.emoji.meaning)
        for f in feedbacks
    ]
    return HistoryResponse(recent_emojis=recent_emojis)
