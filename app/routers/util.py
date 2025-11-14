"""
Shared utility functions for routers.
"""
from fastapi import Request
from app.service.user_class_service import UserClassService
from app.service.fitness_class_service import FitnessClassService

def set_enrolled_classes_in_session(
        request: Request,
        user_id: int,
        user_class_service: UserClassService,
        fitness_class_service: FitnessClassService
):
    """
    Helper function to update the session with enrolled class details,
    including the status from UserClassService.
    """
    enrolled_class_ids = []
    enrolled_classes_models = []

    if user_id:
        enrolled_class_ids = user_class_service.get_enrolled_class_ids(user_id)

        if enrolled_class_ids:
            for class_id in enrolled_class_ids:
                # Skip already paid classes if needed
                if not user_class_service.is_paid(user_id=user_id, class_id=class_id):
                    cls = fitness_class_service.get_class_by_id(class_id)
                    if cls:
                        enrolled_classes_models.append(cls)

    # Build a list of dicts with status
    enrolled_classes_list = []
    for c in enrolled_classes_models:
        status = user_class_service.get_status(user_id, c.id)
        enrolled_classes_list.append({
            "id": c.id,
            "name": c.name,
            "price": c.price,
            "start_time": c.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": c.end_time.strftime("%Y-%m-%d %H:%M"),
            "status": status
        })

    request.session["enrolledClassIds"] = enrolled_class_ids
    request.session["enrolledClasses"] = enrolled_classes_list
