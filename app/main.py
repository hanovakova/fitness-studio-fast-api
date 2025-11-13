import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.routers import auth, check_out, fitness_class, user_class

app = FastAPI()
app.include_router(auth.router)
app.include_router(check_out.router)
app.include_router(fitness_class.router)
app.include_router(user_class.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
