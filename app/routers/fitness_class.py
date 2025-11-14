from typing import Optional, Annotated

from fastapi import APIRouter
from fastapi import Depends, Request, Form
from fastapi.responses import JSONResponse
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


@router.get("/", include_in_schema=False)
async def landing_page():
    """
    Redirects the root URL ("/") to the main fitness classes page.
    """
    return RedirectResponse(url="/fitness-classes")


@router.get("/fitness-classes")
async def show_classes(
        request: Request,
        templates: Templates,
        session: SessionData,
        fitness_class_service: FitnessService,
        user_class_service: UserClassSvc,
        classTime: Optional[str] = None,
        classType: Optional[str] = None
):
    """
    Displays the list of fitness classes, with filtering.
    """
    user_id = session.get("userId")

    # 1. Get and filter classes
    classes = fitness_class_service.get_all_classes()

    if classTime:
        classes = fitness_class_service.get_classes_by_time_frame(classTime, classes)

    if classType:
        classes = fitness_class_service.get_classes_by_class_type(classType, classes)

    # 2. Get enrollment status (paid, capacity)
    class_ids_paid = {}
    class_ids_capacity_exceeded = {}

    if user_id:
        enrolled_class_ids = user_class_service.get_enrolled_class_ids(user_id)
        for class_id in enrolled_class_ids:
            is_paid = user_class_service.is_paid(user_id=user_id, class_id=class_id)
            class_ids_paid[str(class_id)] = is_paid

    for fc in classes:
        class_id = fc.id
        num_signed_up = user_class_service.get_number_of_signups(class_id)
        is_exceeded = fitness_class_service.is_class_capacity_exceeded(class_id, num_signed_up)
        class_ids_capacity_exceeded[str(class_id)] = is_exceeded

    # 3. Update session with enrolled classes (for navbar cart)
    set_enrolled_classes_in_session(
        request, user_id, user_class_service, fitness_class_service
    )

    # 4. Build template context manually
    context = {
        "request": request,
        "session": request.session,  # Get fresh session data after update
        "timeOptions": ["Morning", "Afternoon", "Evening"],
        "typeOptions": {
            "FitnessClass": "Fitness Class",
            "YogaClass": "Yoga",
            "SpinningClass": "Spinning"
        },
        "fitnessClasses": classes,
        "classTime": classTime,
        "classType": classType,
        "classIdsPaid": class_ids_paid,
        "classIdsCapacityExceeded": class_ids_capacity_exceeded,
    }

    return templates.TemplateResponse("fitnessClassesView.html", context)


@router.post("/fitness-classes")
async def sign_up_for_class(
        request: Request,
        fitness_class_service: FitnessService,
        user_class_service: UserClassSvc,
        classId: Annotated[int, Form()]
):
    """
    Handles class sign-up. Returns JSON.
    """
    user_id = request.session.get("userId")
    if not user_id:
        return JSONResponse(
            status_code=401,
            content={"status": "unauthorized"}
        )

    try:
        signups =  user_class_service.get_number_of_signups(classId)
        is_class_capacity_exceeded = fitness_class_service.is_class_capacity_exceeded(classId, signups)
        if not is_class_capacity_exceeded:
            user_class_service.sign_up_for_class(
                user_id=user_id,
                class_id=classId,
            )
            return JSONResponse({"status": "success"})

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
