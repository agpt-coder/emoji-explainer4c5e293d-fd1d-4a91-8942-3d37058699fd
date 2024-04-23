import logging
from contextlib import asynccontextmanager

import project.checkApiStatus_service
import project.createUser_service
import project.deleteFeedback_service
import project.deleteUser_service
import project.explainEmoji_service
import project.fetchEmojiMeaning_service
import project.fetchFeedback_service
import project.getHistory_service
import project.getSupportedEmojis_service
import project.getUserDetails_service
import project.interpretEmoji_service
import project.submitFeedback_service
import project.updateFeedback_service
import project.updateUser_service
import project.userLogin_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="emoji-explainer",
    lifespan=lifespan,
    description="create an endpoint that connects to groq https://console.groq.com and takes in an emoji as input and explains to the user the meaning of it",
)


@app.put(
    "/api/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: int, email: str, name: str, role: project.updateUser_service.Role
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates user details for a specific userId. Accepts fields like email, name, and role in the JSON body. Requires user authentication and only allows the user or an admin to update the data. Returns the updated user information.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, name, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/status", response_model=project.checkApiStatus_service.GetApiStatusResponse
)
async def api_get_checkApiStatus(
    request: project.checkApiStatus_service.GetApiStatusRequest,
) -> project.checkApiStatus_service.GetApiStatusResponse | Response:
    """
    This endpoint provides the current status of the emoji-explainer API. It helps in monitoring whether the API is up and running and can connect to external services like GROQ. The endpoint would simply return a status code and a message indicating the API's health.
    """
    try:
        res = await project.checkApiStatus_service.checkApiStatus(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/emoji/explain", response_model=project.explainEmoji_service.EmojiExplainResponse
)
async def api_post_explainEmoji(
    emoji_character: str,
) -> project.explainEmoji_service.EmojiExplainResponse | Response:
    """
    This POST endpoint receives an emoji as input from the user, sends a request to the GROQ platform to retrieve the explanation and meaning of the provided emoji. The endpoint integrates with the GROQ API, crafting a query based on the received emoji and parsing the GROQ response to format a user-friendly explanation. Expected responses include a success case with the emoji's meaning or a fail case with an error message (e.g., unsupported emoji). This route is essential to allow real-time emoji explanations to users across various devices, owing to the Responsive Design Module's capability to adapt the response format according to the device.
    """
    try:
        res = await project.explainEmoji_service.explainEmoji(emoji_character)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/feedback", response_model=project.fetchFeedback_service.GetFeedbackResponse)
async def api_get_fetchFeedback(
    page: int, limit: int
) -> project.fetchFeedback_service.GetFeedbackResponse | Response:
    """
    This endpoint retrieves all feedback submitted by users. It is protected and periodically fetches data from the database to provide admins with a comprehensive view of user opinions and suggestions on emoji interpretations. The data is returned in a paginated format to manage large volumes of feedback effectively.
    """
    try:
        res = await project.fetchFeedback_service.fetchFeedback(page, limit)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/feedback/{feedbackId}",
    response_model=project.updateFeedback_service.PatchFeedbackResponse,
)
async def api_patch_updateFeedback(
    feedbackId: int, newContent: str, userId: int
) -> project.updateFeedback_service.PatchFeedbackResponse | Response:
    """
    Allows administrators to update existing feedback entries. Users may need to correct or add additional information to their feedback. This endpoint provides flexibility in maintaining accurate and useful data, with access restricted to higher privilege roles to prevent unauthorized modifications.
    """
    try:
        res = project.updateFeedback_service.updateFeedback(
            feedbackId, newContent, userId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a user account for a specified userId. This is a protected route that requires authentication and is only permissible for admin role users. Returns a success message with status code 200 if deletion is successful.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback", response_model=project.submitFeedback_service.FeedbackResponseModel
)
async def api_post_submitFeedback(
    userId: int, emojiId: int, content: str
) -> project.submitFeedback_service.FeedbackResponseModel | Response:
    """
    This endpoint allows users to submit feedback on emoji interpretations. It accepts JSON data containing the emoji and the user's feedback. This data is then sent to the API Communication Module for processing and storage. The endpoint ensures that feedback is collected efficiently and securely, with appropriate validation in place.
    """
    try:
        res = await project.submitFeedback_service.submitFeedback(
            userId, emojiId, content
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/emoji-explainer",
    response_model=project.fetchEmojiMeaning_service.EmojiExplainerResponse,
)
async def api_post_fetchEmojiMeaning(
    emoji: str,
) -> project.fetchEmojiMeaning_service.EmojiExplainerResponse | Response:
    """
    This endpoint allows users to input an emoji and request its meaning from the GROQ API. The route expects an emoji character as input, sends a query to the GROQ API, and returns the explanation of the emoji. It's essential to handle errors gracefully, such as invalid emoji inputs or issues with GROQ API communication.
    """
    try:
        res = await project.fetchEmojiMeaning_service.fetchEmojiMeaning(emoji)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/emoji/supported",
    response_model=project.getSupportedEmojis_service.GETSupportedEmojisResponse,
)
async def api_get_getSupportedEmojis(
    request: project.getSupportedEmojis_service.GETSupportedEmojisRequest,
) -> project.getSupportedEmojis_service.GETSupportedEmojisResponse | Response:
    """
    This GET endpoint provides a list of all emojis that can be interpreted by the system. It queries an internal database through the API Communication Module to retrieve the supported emoji list, ensuring that it is always up-to-date. This endpoint is primarily informational and is used to enhance user experience by informing them of the supported functionalities.
    """
    try:
        res = await project.getSupportedEmojis_service.getSupportedEmojis(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/interpret",
    response_model=project.interpretEmoji_service.EmojiInterpretationResponse,
)
async def api_post_interpretEmoji(
    emoji: str,
) -> project.interpretEmoji_service.EmojiInterpretationResponse | Response:
    """
    This endpoint receives a JSON payload containing an emoji character and sends a request to the Groq API to fetch the interpretation of the emoji. It processes the emoji input, forwards it to the Groq service, and parses the response to provide a meaningful interpretation. The endpoint expects a payload of {'emoji': 'emoji_character'} and returns a JSON object {'meaning': 'explanation_text'}. This service is crucial for delivering the core functionality of the emoji-explainer product.
    """
    try:
        res = await project.interpretEmoji_service.interpretEmoji(emoji)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/feedback/{feedbackId}",
    response_model=project.deleteFeedback_service.DeleteFeedbackResponse,
)
async def api_delete_deleteFeedback(
    feedbackId: int,
) -> project.deleteFeedback_service.DeleteFeedbackResponse | Response:
    """
    This endpoint allows administrators to delete specific feedback entries. It requires a feedback ID as a path parameter. This function ensures that administrators can manage content within the database responsibly, maintaining the integrity and relevance of the feedback data stored.
    """
    try:
        res = await project.deleteFeedback_service.deleteFeedback(feedbackId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/api/history", response_model=project.getHistory_service.HistoryResponse)
async def api_get_getHistory(
    request: project.getHistory_service.HistoryRequest,
) -> project.getHistory_service.HistoryResponse | Response:
    """
    Fetches a list of recently interpreted emojis along with their meanings from the database. This endpoint provides history tracking and retrieval functionality, enhancing user experience by allowing them to view past interpretations. It returns a JSON array of recent interpretations, e.g., [{'emoji': 'emoji_character', 'meaning': 'interpretation_text'}]. This service is intended for use by logged-in users to view their personal emoji interpretation history.
    """
    try:
        res = await project.getHistory_service.getHistory(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/users/{userId}",
    response_model=project.getUserDetails_service.UserDetailsResponse,
)
async def api_get_getUserDetails(
    userId: int,
) -> project.getUserDetails_service.UserDetailsResponse | Response:
    """
    Retrieves detailed information of a user based on the supplied userID in the URL path. Only authenticated and authorized users can access this information. It ensures data safety by allowing only the user or admins to fetch the details.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/users/login", response_model=project.userLogin_service.LoginResponse)
async def api_post_userLogin(
    email: str, password: str
) -> project.userLogin_service.LoginResponse | Response:
    """
    This endpoint allows users to log in. It requires an email and password in the request body. If authentication is successful, it returns a JSON Web Token (JWT) for session management, along with user details.
    """
    try:
        res = await project.userLogin_service.userLogin(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    email: str, password: str, role: project.createUser_service.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This endpoint creates a new user account. It expects a JSON body with user details such as email, password, and role. It returns the created user's details excluding the password, and upon successful creation, returns a status code of 201.
    """
    try:
        res = await project.createUser_service.createUser(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
