import redis
import asyncio
from icecream import ic

async def get_redis_data(key):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.zrange(key, 0, 10, withscores=True)

async def main():
    current_data_bid = await get_redis_data("stock:xyz:bid")
    ic(current_data_bid)
    # current_data_sell = await get_redis_data("stock:xyz:sell")
    # ic(current_data_bid)
    # ic(current_data_sell)

asyncio.run(main())
