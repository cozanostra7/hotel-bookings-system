import redis.asyncio as redis
from typing import Optional, Any


class RedisManager:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        decode_responses: bool = True,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        self._client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=self.decode_responses,
        )
        await self._client.ping()

    async def close(self) -> None:
        if self._client:
            await self._client.close()

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = None,
    ) -> None:

        if not self._client:
            raise RuntimeError("Redis is not connected")

        await self._client.set(name=key, value=value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        if not self._client:
            raise RuntimeError("Redis is not connected")

        return await self._client.get(name=key)

    async def delete(self, key: str) -> None:
        if not self._client:
            raise RuntimeError("Redis is not connected")

        await self._client.delete(key)

