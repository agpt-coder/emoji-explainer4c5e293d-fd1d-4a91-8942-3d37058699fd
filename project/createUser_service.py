from datetime import datetime, timezone
from enum import Enum

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum type defining possible roles: ADMIN, USER, GUEST.
    """

    pass


class CreateUserResponse(BaseModel):
    """
    Response model for the newly created user account. It returns user details relevant to their profile but excluded sensitive data like the password.
    """

    id: int
    email: str
    role: str
    createdAt: datetime


async def hash_password(password: str) -> str:
    """
    Hashes the password using bcrypt for secure storage.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


async def createUser(email: str, password: str, role: Role) -> CreateUserResponse:
    """
    Creates a new user account with the given email, password, and role. Returns structured data
    about the newly created user excluding the password.

    Args:
        email (str): The email address for the new user account, used as the primary means of identification.
        password (str): The password for securing the user's account. This will be hashed and not stored directly.
        role (Role): The role assigned to the user which can be either ADMIN, USER, or GUEST.

    Returns:
        CreateUserResponse: Response containing the newly created user's data.
    """
    hashed_password = await hash_password(password)
    user_data = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password, "role": role.name}
    )
    created_datetime = datetime.now(timezone.utc)
    return CreateUserResponse(
        id=user_data.id,
        email=user_data.email,
        role=user_data.role,
        createdAt=created_datetime,
    )
