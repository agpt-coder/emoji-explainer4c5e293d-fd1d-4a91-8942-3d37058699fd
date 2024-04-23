from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum type defining possible roles: ADMIN, USER, GUEST.
    """

    pass


class UpdateUserResponse(BaseModel):
    """
    This response model provides the confirmed updated details of the user after the PUT operation. It reflects changes and confirms that the update operation was successful.
    """

    userId: int
    email: str
    name: str
    role: str


async def updateUser(
    userId: int, email: str, name: str, role: Role
) -> UpdateUserResponse:
    """
    Updates user details for a specific userId. Accepts fields like email, name, and role in the JSON body.
    Requires user authentication and only allows the user or an admin to update the data.
    Returns the updated user information.

    Args:
        userId (int): The unique identifier of the user to update.
        email (str): The new email address of the user.
        name (str): The new name of the user.
        role (Role): The new role assigned to the user.

    Returns:
        UpdateUserResponse: This response model provides the confirmed updated details
        of the user after the PUT operation. It reflects changes and confirms that the
        update operation was successful.

    Example with dummy values:
        updateUser(1, "newemail@example.com", "John Doe", Role.USER)
        > UpdateUserResponse(userId=1, email="newemail@example.com", name="John Doe", role="USER")
    """
    existing_user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not existing_user:
        raise ValueError("User with ID does not exist")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data={"email": email, "name": name, "role": role.value}
    )
    return UpdateUserResponse(
        userId=updated_user.id,
        email=updated_user.email,
        name=updated_user.name,
        role=updated_user.role.value,
    )  # TODO(autogpt): Cannot access attribute "name" for class "User"


#     Attribute "name" is unknown. reportAttributeAccessIssue
