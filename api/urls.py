from ninja_extra import NinjaExtraAPI

from api.users.api import AuthController, UserController
from api.posts.api import PostController
from api.comments.api import CommentController, AnalyticsController

api = NinjaExtraAPI(
    title="Starnavi Test API",
    version="1.0.0",
    description="API description",
)

api.register_controllers(
    AuthController,
    UserController,
    PostController,
    CommentController,
    AnalyticsController,
)
