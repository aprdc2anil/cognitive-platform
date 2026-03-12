from core.database.postgres import get_connection
from core.redis.redis import get_redis
from core.logging.logger import logger


logger.info("testing_platform_core")

conn = get_connection()
print("Postgres connected")
conn.close()

r = get_redis()
print("Redis ping:", r.ping())
