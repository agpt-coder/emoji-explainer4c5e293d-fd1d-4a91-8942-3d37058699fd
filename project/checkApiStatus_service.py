from httpx import AsyncClient
from pydantic import BaseModel


class GetApiStatusRequest(BaseModel):
    """
    GET request model for the /api/status endpoint. This model does not need any specific input parameters as it is merely used to check system status.
    """

    pass


class GetApiStatusResponse(BaseModel):
    """
    Defines the response structure for the /api/status endpoint, which provides insights into the API's current operational status.
    """

    status_code: int
    message: str


async def checkApiStatus(request: GetApiStatusRequest) -> GetApiStatusResponse:
    """
    This endpoint provides the current status of the emoji-explainer API. It helps in monitoring whether the API is up and running and can connect to external services like GROQ. The endpoint would simply return a status code and a message indicating the API's health.

    Args:
        request (GetApiStatusRequest): GET request model for the /api/status endpoint. This model does not need any specific input parameters as it is merely used to check system status.

    Returns:
        GetApiStatusResponse: Defines the response structure for the /api/status endpoint, which provides insights into the API's current operational status.

    Example:
        request = GetApiStatusRequest()
        response = await checkApiStatus(request)
        print(response.status_code, response.message)
    """
    url = "https://console.groq.com/api/status"
    async with AsyncClient() as client:
        try:
            response = await client.get(url)
            status_code = response.status_code
            if status_code == 200:
                message = "API is operational."
            else:
                message = "API is experiencing issues."
            return GetApiStatusResponse(status_code=status_code, message=message)
        except Exception as e:
            return GetApiStatusResponse(status_code=503, message=str(e))
