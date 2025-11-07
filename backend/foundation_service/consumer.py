from aiokafka import AIOKafkaConsumer
import asyncio
import json
import logging

from shared.core.security import settings
from shared.db.engine import get_db
from crud import pay_to_found


logger = logging.getLogger(__name__)


class ConsumerManager:
    def __init__(self) -> None:
        self.consumer = None
        self.running = False

    
    async def start(self, topic: str):
        try:
            self.consumer = AIOKafkaConsumer(
                topic,
                loop=asyncio.get_event_loop(),
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
            )
            await self.consumer.start()
            self.running = True
            logger.info(f"Kafka konsumer started topic: {topic}")

        except Exception as e:
            raise e
    
    async def stop(self):
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")


    async def consume_messages(self):
        try:
            if self.consumer is None:
                logger.error("You have to consumer started")
                raise

            async for msg in self.consumer:
                logger.info(f"Received message: {msg.value}")

                user_id = msg.value.get('user_id')
                amount = msg.value.get('amount')
                found_id = msg.value.get('found_id')
                
                logger.info(f"Processing payment: user_id={user_id}, amount={amount}, found_id={found_id}")

                async for session in get_db():
                    try:
                        await pay_to_found(
                            session=session,
                            user_id=user_id,
                            found_id = found_id,
                            amount=amount
                        )
                        logger.info(f"Successfully updated foundation {found_id} with amount {amount}")

                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                    finally:
                        break  

            


        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
            raise


kafka_consumer = ConsumerManager()


async def start_consumer(topic: str):
    await kafka_consumer.start(topic)
    await kafka_consumer.consume_messages()