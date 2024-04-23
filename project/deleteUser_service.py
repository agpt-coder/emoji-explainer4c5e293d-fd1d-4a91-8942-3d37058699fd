import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    This communicates the successful deletion of a user or failure thereof, without disclosing sensitive user information.
    """

    message: str
    status: int


async def deleteUser(userId: str) -> DeleteUserResponse:
    """
    Deletes a user account for a specified userId. This is a protected route that requires authentication and is only permissible for admin role users. Returns a success message with status code 200 if deletion is successful.

    Args:
        userId (str): The unique identifier of the user to be deleted.

    Returns:
        DeleteUserResponse: This communicates the successful deletion of a user or failure thereof, without disclosing sensitive user information.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": int(userId)})
    if not user:
        return DeleteUserResponse(message="User not found.", status=404)
    if user.role != prisma.enums.Role.ADMIN:
        return DeleteUserResponse(
            message="Unauthorized access. Only admin users can delete accounts.",
            status=403,
        )
    await prisma.models.User.prisma().delete(where={"id": int(userId)})
    return DeleteUserResponse(message="User successfully deleted.", status=200)
