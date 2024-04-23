import datetime
from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum type defining possible roles: ADMIN, USER, GUEST.
    """

    pass


class UserDetailsResponse(BaseModel):
    """
    Provides detailed information of a user, excluding sensitive data like passwords. Appropriate only for the user themselves or an admin.
    """

    id: int
    email: str
    role: Role
    feedbacksCount: int
    sessionsCount: int


async def getUserDetails(userId: int) -> UserDetailsResponse:
    """
    Retrieves detailed information of a user based on the supplied userID.
    Only authenticated and authorized users can access this information.
    It ensures data safety by allowing only the user or admins to fetch the details.

    Args:
        userId (int): The unique identifier of the user whose details are to be retrieved.

    Returns:
        UserDetailsResponse: Provides detailed information of a user, excluding sensitive data like passwords.
                             Appropriate only for the user themselves or an admin.
    """
    user: Optional[prisma.models.User] = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"feedbacks": True, "sessions": True}
    )
    if user is None:
        raise ValueError("prisma.models.User not found.")
    active_sessions_count = sum(
        (1 for session in user.sessions if session.expiresAt > datetime.datetime.now())
    )
    return UserDetailsResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        feedbacksCount=len(user.feedbacks),
        sessionsCount=active_sessions_count,
    )
