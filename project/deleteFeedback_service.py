import prisma
import prisma.models
from pydantic import BaseModel


class DeleteFeedbackResponse(BaseModel):
    """
    This model defines the structure of the response after attempting to delete a feedback. It will confirm whether the deletion was successful.
    """

    success: bool
    message: str


async def deleteFeedback(feedbackId: int) -> DeleteFeedbackResponse:
    """
    This endpoint allows administrators to delete specific feedback entries. It requires a feedback ID as a path parameter. This function ensures that administrators can manage content within the database responsibly, maintaining the integrity and relevance of the feedback data stored.

    Args:
        feedbackId (int): The unique identifier for the feedback entry to be deleted.

    Returns:
        DeleteFeedbackResponse: This model defines the structure of the response after attempting to delete a feedback. It will confirm whether the deletion was successful.
    """
    feedback = await prisma.models.Feedback.prisma().find_unique(
        where={"id": feedbackId}
    )
    if feedback is None:
        return DeleteFeedbackResponse(
            success=False, message=f"No feedback found with ID {feedbackId}"
        )
    if feedback.reviewed:
        return DeleteFeedbackResponse(
            success=False,
            message=f"Feedback {feedbackId} has been reviewed and cannot be deleted",
        )
    delete_result = await prisma.models.Feedback.prisma().delete(
        where={"id": feedbackId}
    )
    if delete_result:
        return DeleteFeedbackResponse(
            success=True, message=f"Feedback {feedbackId} successfully deleted."
        )
    else:
        return DeleteFeedbackResponse(
            success=False, message="Deletion failed due to a server error."
        )
