from ninja_extra import NinjaExtraAPI

from api.posts.api.post import PostController
from api.users.api import AuthController, UserController

api = NinjaExtraAPI(
    title="Starnavi Test API",
    version="1.0.0",
    description="API description",
)

api.register_controllers(
    AuthController,
    UserController,
    PostController,
)
