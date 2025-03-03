import typing
import strawberry
from strawberry.permission import BasePermission
from fastapi import Request

from aquasensor_backend.security import get_logged_in_user

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    # This method can also be async!
    async def has_permission(
        self, source: typing.Any, info: strawberry.Info, **kwargs
    ) -> bool:
        
        info.context["user"] = None

        request: Request = info.context.get("request")
        
        # this should never happen
        if not request:
            return False
        
        # check if the request has an api key
        api_key = request.headers.get("AquaSensor-Login-Token")
        if not api_key:
            return False
        
        # check if the api key is valid
        user = await get_logged_in_user(api_key)

        info.context["user"] = user

        return user