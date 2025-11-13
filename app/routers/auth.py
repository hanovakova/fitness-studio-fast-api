from typing import Annotated

from fastapi import (
    APIRouter, Depends, Request, Form
)
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.dependencies import (
    user_service, templates, get_session_data
)
from app.pydantic_models import UserCreate, RegistrationForm
from app.service.user_service import UserService

router = APIRouter()

# --- Type Hints for Dependencies ---
Templates = Annotated[Jinja2Templates, Depends(templates)]
SessionData = Annotated[dict, Depends(get_session_data)]
UserServiceDep = Annotated[UserService, Depends(user_service)]


@router.get("/login", response_class=HTMLResponse)
async def show_login_page(
        request: Request,
        templates: Templates,
        session: SessionData
):
    """Serves the login page."""
    context = {"request": request, "session": session}
    return templates.TemplateResponse("loginView.html", context)


@router.post("/login")
async def login(
        request: Request,
        templates: Templates,
        session: SessionData,
        user_service: UserServiceDep,
        username: Annotated[str, Form()],
        password: Annotated[str, Form()]
):
    """Handles login form submission."""
    try:
        user = user_service.validate_user(username, password)
        if user:
            # Set session attributes
            request.session["userId"] = user.id
            request.session["username"] = user.username
            request.session["loggedIn"] = True
            return RedirectResponse(url="/confirmation", status_code=303)
        else:
            # Re-render login page with error
            context = {
                "request": request,
                "session": session,
                "error": "Invalid username or password",
                "username": username
            }
            return templates.TemplateResponse("loginView.html", context, status_code=400)
    except Exception as e:
        context = {
            "request": request,
            "session": session,
            "error": f"An error occurred: {e}"
        }
        return templates.TemplateResponse("loginView.html", context, status_code=500)


@router.post("/logout")
async def logout(request: Request):
    """Clears the session and redirects."""
    request.session.clear()
    return RedirectResponse(url="/fitness-classes", status_code=303)


@router.get("/confirmation", response_class=HTMLResponse)
async def show_confirmation_page(
        request: Request,
        templates: Templates,
        session: SessionData
):
    """Shows the registration confirmation page."""
    context = {"request": request, "session": session}
    return templates.TemplateResponse("registrationConfirmedView.html", context)


@router.get("/register", response_class=HTMLResponse)
async def show_register_form(
        request: Request,
        templates: Templates,
        session: SessionData
):
    """Serves the registration page."""
    context = {"request": request, "session": session, "errors": {}, "form_data": {}}
    return templates.TemplateResponse("registerView.html", context)


@router.post("/register")
async def register(
        request: Request,
        templates: Templates,
        session: SessionData,
        user_service: UserServiceDep,
):
    """
    Handles registration form submission.
    Matches the `users.py` validation pattern.
    """
    form_data = dict(await request.form())

    try:
        # 1. Validate form data using Pydantic schema
        form = RegistrationForm(**form_data)

    except ValidationError as exc:
        # Pydantic validation failed, re-render form with errors
        error_messages = {}
        for error in exc.errors():
            loc = error.get('loc')
            if loc:
                error_messages[loc[0]] = error['msg']
            elif "Passwords do not match" in error['msg']:
                error_messages['password2'] = "Passwords do not match"

        # Clear passwords
        form_data['password'] = ''
        form_data['password2'] = ''

        context = {
            "request": request,
            "session": session,
            "errors": error_messages,
            "form_data": form_data
        }
        return templates.TemplateResponse("registerView.html", context, status_code=400)

    # 3. Create user in database
    try:
        user_create_schema = UserCreate(
            username=form.username,
            password=form.password,  # Service will hash this
            email=form.email,
            name=form.name,
            advertisement=form.advertisement,
        )
        new_user = user_service.create_user(user_create_schema)

        # 4. Set session and redirect
        request.session["userId"] = new_user.id
        request.session["username"] = new_user.username
        request.session["loggedIn"] = True

        return RedirectResponse(url="/confirmation", status_code=303)

    except ValueError as e:
        # Handle "Username already registered"
        errors = {"username": str(e)}
        context = {"request": request, "session": session, "errors": errors, "form_data": form_data}
        return templates.TemplateResponse("registerView.html", context, status_code=400)
