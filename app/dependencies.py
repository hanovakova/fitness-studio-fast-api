from starlette.requests import Request
from starlette.templating import Jinja2Templates

from app.messaging.rabbit_client import RabbitMQClient
from app.repository.fitness_class_repo import FitnessClassRepository
from app.repository.user_class_repo import UserClassRepository
from app.repository.user_repo import UserRepository
from app.service.fitness_class_service import FitnessClassService
from app.service.user_class_service import UserClassService
from app.service.user_service import UserService

REQUEST_QUEUE: str = "purchase_requests"
RESPONSE_QUEUE: str = "purchase_responses"

jinja_templates = Jinja2Templates(directory="templates")
def templates():
    return jinja_templates

obj_user_service = UserService(UserRepository())
obj_user_class_service = UserClassService(UserClassRepository())
obj_fitness_class_service = FitnessClassService(FitnessClassRepository())

def user_service():
    return obj_user_service

def user_class_service():
    return obj_user_class_service

def fitness_class_service():
    return obj_fitness_class_service

def get_session_data(request: Request) -> dict:
    """
    Dependency to get global session attributes.
    This replaces `get_cart` from your example.
    """
    return {
        "loggedIn": request.session.get("loggedIn", False),
        "username": request.session.get("username"),
        "userId": request.session.get("userId"),
        "enrolledClasses": request.session.get("enrolledClasses", []),
        "avatar": request.session.get("avatar")
    }

async def get_rabbit_client():
    client = RabbitMQClient(queue=REQUEST_QUEUE)
    try:
        await client.connect()
        yield client
    finally:
        await client.close()
