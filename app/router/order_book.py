
import redis
import asyncio
# import redis.asyncio as redis
from fastapi import WebSocket,WebSocketDisconnect, APIRouter
from icecream import ic

router = APIRouter(
    prefix="/order_book",
    tags=["order_book"],
)

async def get_redis_data(key):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.zrange(key, 0, 10, withscores=True)


@router.websocket("/{stock}")
async def order_book(websocket: WebSocket, stock: str):
    await websocket.accept()

    try:
        prev_data = ""
        unchanged_count = 0
        max_unchanged_threshold = 5  # Adjust this threshold as needed

        while True:
            current_data_bid = await get_redis_data(f"stock:{stock}:bid")
            current_data_sell = await get_redis_data(f"stock:{stock}:sell")

            # Extract data from the Redis objects
            current_data_bid_values = [item[0] for item in current_data_bid]
            current_data_sell_values = [item[0] for item in current_data_sell]


            # Combine the data into a single string for sending
            current_data = f"Bid: {current_data_bid_values}, Sell: {current_data_sell_values}"
            
            ic(current_data)

            if prev_data != current_data:
                # Reset the counter if data changes
                unchanged_count = 0
                
                # Send data to the WebSocket
                prev_data = current_data
                await websocket.send_text(current_data)
            else:
                unchanged_count += 1

                if unchanged_count >= max_unchanged_threshold:
                    # If unchanged for too long, sleep for a longer duration
                    await asyncio.sleep(5)
                else:
                    # Otherwise, sleep for a short duration
                    await asyncio.sleep(1)

    except WebSocketDisconnect:
        # Handle disconnection if needed
        pass

