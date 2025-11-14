import json
from typing import Optional

import aio_pika


class RabbitMQClient:
    def __init__(self, queue: str, host: str = "localhost"):
        self.host = host
        self.queue_name = queue
        self.connection: Optional[aio_pika.RobustConnection] = None
        self.channel: Optional[aio_pika.RobustChannel] = None
        self.exchange: Optional[aio_pika.Exchange] = None

    async def connect(self):
        """Establish connection and channel, declare queue."""
        self.connection = await aio_pika.connect_robust(f"amqp://guest:guest@{self.host}/")
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        # Declare a queue (durable)
        await self.channel.declare_queue(self.queue_name, durable=True)
        print(f"[RabbitMQ] Connected to queue '{self.queue_name}' on {self.host}")

    async def send_message(self, message: dict):
        """Send a JSON-serializable dict as a persistent RabbitMQ message."""
        if not self.channel:
            raise RuntimeError("Connection not established. Call 'await connect()' first.")

        body = json.dumps(message).encode("utf-8")
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=self.queue_name
        )
        print(f"[RabbitMQ] Message sent: {json.dumps(message)}")

    async def close(self):
        """Close connection."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            print("[RabbitMQ] Connection closed.")
