from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class FeedbackDetail(BaseModel):
    """
    Detailed structure for representing feedback which includes the user's email and the content of the feedback.
    """

    id: int
    content: str
    userEmail: str
    createdAt: datetime


class GetFeedbackResponse(BaseModel):
    """
    This model represents the paginated response that includes user feedback details. The response includes pagination details to assist clients in navigating the data.
    """

    feedbacks: List[FeedbackDetail]
    totalPages: int
    currentPage: int


async def fetchFeedback(page: int, limit: int) -> GetFeedbackResponse:
    """
    This endpoint retrieves all feedback submitted by users. It is protected and periodically fetches data from the database to provide admins with a comprehensive view of user opinions and suggestions on emoji interpretations. The data is returned in a paginated format to manage large volumes of feedback.

    Args:
    page (int): The page number of feedback results to be displayed.
    limit (int): The number of feedback entries to retrieve per page.

    Returns:
    GetFeedbackResponse: This model represents the paginated response that includes user feedback details. The response includes pagination details to assist clients in navigating the data.
    """
    skip = (page - 1) * limit
    feedback_records = await prisma.models.Feedback.prisma().find_many(
        skip=skip, take=limit, include={"user": True}, order={"createdAt": "desc"}
    )
    total_feedback_count = await prisma.models.Feedback.prisma().count()
    total_pages = (total_feedback_count + limit - 1) // limit
    feedback_details = [
        FeedbackDetail(
            id=record.id,
            content=record.content,
            userEmail=record.user.email,
            createdAt=record.createdAt,
        )
        for record in feedback_records
    ]
    return GetFeedbackResponse(
        feedbacks=feedback_details, totalPages=total_pages, currentPage=page
    )
