import aioredis
import redis
import asyncio

async def publish_update(stock_name, update_data):
    redis_conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
    channel_name = f"stock:{stock_name}"

    try:
        # Publish the update to the Redis channel
        await redis_conn.execute_pubsub('PUBLISH', channel_name, update_data)
    except aioredis.RedisError as e:
        print(f"Error publishing update: {e}")
    finally:
        # Close the connection
        redis_conn.close()
        # await redis_conn.wait_closed()

# Example usage of the publishing code
async def main():
    await publish_update("AAPL", "New bid data: ...")

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
