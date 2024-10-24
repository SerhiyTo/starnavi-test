from django.http import HttpRequest
from ninja_extra import exceptions


class UserService:
    @staticmethod
    async def get_user_id(request: HttpRequest) -> int:
        """
        Get the user ID from the request.

        :param request: request object.
        :return: user ID.
        """
        return request.user.pk if request.user else None

    @staticmethod
    async def check_author_permission(obj_author_id: int, author_id: int) -> None:
        """
        Check if the user has permission to perform an action.

        :param obj_author_id: object with an author field.
        :param author_id: author ID.
        :return: True if the user has permission, False otherwise.
        """
        if obj_author_id != author_id:
            raise exceptions.PermissionDenied("You are not the author of this post.")
