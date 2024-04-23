import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackResponseModel(BaseModel):
    """
    Response model confirming the receipt and handling of the user feedback.
    """

    success: bool
    message: str


async def submitFeedback(
    userId: int, emojiId: int, content: str
) -> FeedbackResponseModel:
    """
    This endpoint allows users to submit feedback on emoji interpretations. It accepts JSON data containing the emoji and the user's feedback. This data is then sent to the API Communication Module for processing and storage. The endpoint ensures that feedback is collected efficiently and securely, with appropriate validation in place.

    Args:
    userId (int): ID of the user providing feedback.
    emojiId (int): ID of the emoji the feedback is about.
    content (str): The textual feedback provided by the user.

    Returns:
    FeedbackResponseModel: Response model confirming the receipt and handling of the user feedback.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return FeedbackResponseModel(success=False, message="User not found")
    emoji = await prisma.models.Emoji.prisma().find_unique(where={"id": emojiId})
    if not emoji:
        return FeedbackResponseModel(success=False, message="Emoji not found")
    feedback = await prisma.models.Feedback.prisma().create(
        data={"userId": userId, "emojiId": emojiId, "content": content}
    )
    if feedback:
        return FeedbackResponseModel(
            success=True, message="Feedback received successfully"
        )
    else:
        return FeedbackResponseModel(success=False, message="Failed to submit feedback")
