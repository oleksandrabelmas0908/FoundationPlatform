from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio

from shared.core.security import settings


class KafkaManager:
    def __init__(self, bootstrap: str = settings.KAFKA_BOOTSTRAP_SERVERS) -> None:
        self.bootsrap = bootstrap
        self.loop = asyncio.get_event_loop()

    async def send_one(self, topic: str, message:str) -> None:
        try:
            producer = AIOKafkaProducer(
                loop=self.loop,
                bootstrap_servers=self.bootsrap
            )
            
            try:
                await producer.send_and_wait(topic=topic, value=message)
            finally:
                await producer.stop()

        except Exception as ex:
            raise ex
        
    async def consume(self, topic: str) -> list:
        try:
            consumer = AIOKafkaConsumer(
                topic,
                loop=self.loop,
                bootstrap_servers=self.bootsrap
            )

            try:
                result = []

                await consumer.start()

                async for msg in consumer:
                    result.append(msg)
                
                return result

            except Exception as e:
                raise e
            
            finally:
                await consumer.stop()

        except Exception as e:
            raise e