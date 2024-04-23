from enum import Enum

import jwt
import prisma
import prisma.models
from passlib.hash import bcrypt
from pydantic import BaseModel


class Role(Enum):
    """
    Enum type defining possible roles: ADMIN, USER, GUEST.
    """

    pass


class UserDetails(BaseModel):
    """
    Detailed descriptor of a user including non-sensitive data only.
    """

    email: str
    role: Role


class LoginResponse(BaseModel):
    """
    This response model provides the JWT necessary for session management along with some essential user details post successful authentication.
    """

    jwt: str
    userDetails: UserDetails


async def userLogin(email: str, password: str) -> LoginResponse:
    """
    This endpoint allows users to log in. It requires an email and password in the request body. If authentication is successful, it returns a JSON Web Token (JWT) for session management, along with user details.

    Args:
        email (str): The registered email of the user trying to log in.
        password (str): The password for the associated email, which will be checked during the authentication process.

    Returns:
        LoginResponse: This response model provides the JWT necessary for session management along with some essential user details post successful authentication.

    Raises:
        ValueError: If the username or password do not match.
    """
    user = await prisma.models.User.prisma().find_first(where={"email": email})
    if user is None or not bcrypt.verify(password, user.password):
        raise ValueError("Invalid email or password")
    jwt_token = jwt.encode(
        {"user_id": user.id, "role": user.role.name}, "secret_key", algorithm="HS256"
    )
    user_details = UserDetails(email=user.email, role=user.role)
    return LoginResponse(jwt=jwt_token, userDetails=user_details)
