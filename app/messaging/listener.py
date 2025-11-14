import json
import asyncio
import aio_pika

class Listener:
    """
    Async RabbitMQ listener for lab work.
    Receives purchase events, prints them,
    allows user to approve/reject in console,
    and sends response back.
    """

    def __init__(self, host: str = "localhost"):
        self.host = host
        self.request_queue = "purchase_requests"
        self.response_queue = "purchase_responses"
        self.connection: aio_pika.RobustConnection | None = None
        self.channel: aio_pika.RobustChannel | None = None

    async def connect(self):
        """Connect to RabbitMQ and declare queues."""
        self.connection = await aio_pika.connect_robust(f"amqp://guest:guest@{self.host}/")
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        # Declare queues (durable)
        await self.channel.declare_queue(self.request_queue, durable=True)
        await self.channel.declare_queue(self.response_queue, durable=True)

        print(f"[Listener] Connected to RabbitMQ at {self.host}")
        print(f"[Listener] Waiting for messages on '{self.request_queue}'...")

    async def start(self):
        """Start listening for purchase events."""
        if not self.channel:
            await self.connect()

        queue = await self.channel.declare_queue(self.request_queue, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():  # auto-acknowledge
                    event = json.loads(message.body)
                    print("\n=== New Purchase Event ===")
                    print(json.dumps(event, indent=2))

                    # Ask user in console
                    choice = input("Approve purchase? (y/n): ").strip().lower()
                    status = "Approved" if choice == "y" else "Rejected"

                    response = {
                        "purchase_id": event["purchase_id"],
                        "user_id": event["user_id"],
                        "status": status,
                        "class_ids": [cls.get("id") for cls in event.get("classes", [])]
                    }

                    await self.channel.default_exchange.publish(
                        aio_pika.Message(
                            body=json.dumps(response).encode("utf-8"),
                            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                        ),
                        routing_key=self.response_queue
                    )

                    print(f"[Listener] Sent response: {response}")

    async def close(self):
        """Close RabbitMQ connection."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("[Listener] Connection closed.")


listener = Listener()
asyncio.run(listener.start())
