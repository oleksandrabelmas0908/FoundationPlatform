from aiokafka import AIOKafkaProducer
import asyncio
import json

from shared.core.settings import settings


async def send_one(topic: str, message: dict):
    try:
        producer = AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        try:
            await producer.start()
            await producer.send_and_wait(topic=topic, value=message)
        finally:
            await producer.stop()

    except Exception as ex:
        raise ex