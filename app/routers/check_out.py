import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.dependencies import templates, fitness_class_service, user_class_service, get_session_data, get_rabbit_client
from app.messaging.rabbit_client import RabbitMQClient
from app.pydantic_models import FitnessClassDTO
from app.service.fitness_class_service import FitnessClassService
from app.service.user_class_service import UserClassService

router = APIRouter()

Templates = Annotated[Jinja2Templates, Depends(templates)]
SessionData = Annotated[dict, Depends(get_session_data)]
FitnessService = Annotated[FitnessClassService, Depends(fitness_class_service)]
UserClassSvc = Annotated[UserClassService, Depends(user_class_service)]


@router.get("/checkout")
async def show_checkout_page(
        request: Request,
        templates: Templates,
        session: SessionData
):
    """
    Shows the checkout view.
    """
    context = {"request": request, "session": session}
    return templates.TemplateResponse("checkoutView.html", context)


@router.post("/checkout")
async def process_checkout(
        request: Request,
        fitness_class_service: FitnessService,
        user_class_service: UserClassSvc,
        rabbit_client: RabbitMQClient = Depends(get_rabbit_client)
):
    """
    Processes the checkout, marks items for purchase, and sends to queue.
    """
    user_id = request.session.get("userId")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # 1. Get unpaid classes
    unpaid_class_ids = user_class_service.get_unpaid_class_ids(user_id)

    if not unpaid_class_ids:
        return RedirectResponse(url="/user-classes/purchased", status_code=303)

    # 2. Collect classes and sum
    unpaid_classes_models = []
    purchase_sum = 0.0

    for class_id in unpaid_class_ids:
        fc = fitness_class_service.get_class_by_id(class_id)
        if fc:
            unpaid_classes_models.append(fc)
            if fc.price:
                purchase_sum += fc.price

    unpaid_classes_dto = []

    for cls in unpaid_classes_models:
        cls_dict = {
            "id": cls.id,
            "name": cls.name,
            "price": cls.price,
            "start_time": cls.start_time,
            "end_time": cls.end_time,
            "class_type": getattr(cls, "class_type", None),
            "yoga_level": getattr(cls, "yoga_level", None),
            "bike_type": getattr(cls, "bike_type", None),
        }
        dto = FitnessClassDTO.model_validate(cls_dict)
        unpaid_classes_dto.append(dto)

    # 4. Create event payload (RabbitMQ uses dict, not Pydantic model)
    purchase_dict = {
        "purchase_id": str(uuid.uuid4()),
        "user_id": user_id,
        "classes": [dto.model_dump(mode="json") for dto in unpaid_classes_dto],
        "total_sum": purchase_sum,
    }

    for class_id in unpaid_class_ids:
        user_class_service.update_status(user_id, class_id, "In process")


    # 6. Store pending classes in session
    pending_classes_list = [
        {"id": c.id, "name": c.name, "price": c.price}
        for c in unpaid_classes_models
    ]
    request.session["pendingClasses"] = pending_classes_list

    # 5. Send to RabbitMQ
    try:
        await rabbit_client.send_message(purchase_dict)
    except Exception as e:
        print(f"ERROR: Failed to send purchase message to queue: {e}")
    finally:
        await rabbit_client.close()

    return RedirectResponse(url="/user-classes/purchased", status_code=303)
