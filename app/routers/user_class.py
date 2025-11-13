from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, Request, Form
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.dependencies import templates, fitness_class_service, user_class_service, get_session_data
from app.routers.util import set_enrolled_classes_in_session
from app.service.fitness_class_service import FitnessClassService
from app.service.user_class_service import UserClassService

router = APIRouter()

Templates = Annotated[Jinja2Templates, Depends(templates)]
SessionData = Annotated[dict, Depends(get_session_data)]
FitnessService = Annotated[FitnessClassService, Depends(fitness_class_service)]
UserClassSvc = Annotated[UserClassService, Depends(user_class_service)]


@router.get("/user-classes/selected")
async def view_selected_classes(
        request: Request,
        templates: Templates,
        fitness_class_service: FitnessService,
        user_class_service: UserClassSvc
):
    """
    Shows the user's "cart" of selected, unpaid classes.
    """
    user_id = request.session.get("userId")

    # Update session data
    set_enrolled_classes_in_session(
        request, user_id, user_class_service, fitness_class_service
    )

    # Build context manually with fresh session
    context = {"request": request, "session": request.session}

    return templates.TemplateResponse("selectedClassesView.html", context)


@router.post("/user-classes/drop")
async def drop_class(
        request: Request,
        user_class_service: UserClassSvc,
        enrolledClassId: Annotated[int, Form()]
):
    """
    Handles dropping a class from the user's cart.
    """
    user_id = request.session.get("userId")
    if user_id:
        user_class_service.drop_class(
            user_id=user_id,
            class_id=enrolledClassId
        )

    return RedirectResponse(url="/user-classes/selected", status_code=303)


@router.get("/user-classes/purchased")
async def view_purchased_classes(
        request: Request,
        templates: Templates,
        session: SessionData
):
    """
    Shows the confirmation page after checkout.
    """
    # Get and remove pendingClasses from session
    pending_classes = request.session.pop("pendingClasses", [])

    context = {
        "request": request,
        "session": session,
        "pendingClasses": pending_classes
    }
    return templates.TemplateResponse("purchasedClassesView.html", context)
