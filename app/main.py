import asyncio
import json
from contextlib import asynccontextmanager

import aio_pika
import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from app.dependencies import user_class_service, RESPONSE_QUEUE
from app.routers import auth, check_out, fitness_class, user_class
from app.service.user_class_service import UserClassService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: run the listener in a background task
    Shutdown: cancel it gracefully
    """
    # Create a background task for the listener
    user_class_srv = user_class_service()
    listener_task = asyncio.create_task(listen_results(user_class_srv))

    try:
        yield  # app starts here
    finally:
        # On shutdown, cancel the listener
        listener_task.cancel()
        try:
            await listener_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(check_out.router)
app.include_router(fitness_class.router)
app.include_router(user_class.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


async def listen_results(user_class_srv: UserClassService):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare the queue (durable)
    queue = await channel.declare_queue(RESPONSE_QUEUE, durable=True)
    print(f"[Listener] Waiting for messages on '{RESPONSE_QUEUE}'...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():  # auto-ack
                result = json.loads(message.body)
                print("[Listener] Main app got:", result)

                user_id = result["user_id"]
                class_ids = result.get("class_ids", [])  # may or may not be included
                status = result["status"]

                # Update DB
                for cid in class_ids:
                    user_class_srv.update_status(user_id, cid, status)

                if status == "Approved":
                    for cid in class_ids:
                        user_class_srv.set_payment_status(user_id, cid, True)

                print(f"[Listener] Updated status '{status}' for user {user_id} classes {class_ids}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
