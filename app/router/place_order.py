from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

# from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from .. import schemas, models
import redis



router = APIRouter(
    prefix="/place_order",
    tags=['place_order']
)


# place order
"""
{   
    "stock": "AAPL",
    "price": 100, 
    "quantity": 10,
    "order_type": "buy" # buy or sell
    "order_format": "limit | market"
    
    # no care what the price is when order_format is market
}
"""

def fillOrders(order_format:str, price:int, quantity:int, user_id: int):
    pass
    
# add data to the stocks buy and sell sorted set
async def set_redis_data(key, value, score):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r.zadd(key, score, value)

# route to get a order 
@router.post("/")
async def some(order: schemas.OrderSchema, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    myStock = db.query(models.stocks).filter(models.stocks.StockID == order.stock)     
    if myStock == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"stock doesn't exists")

    remaining = fillOrders(order.order_format, order.price, order.quantity, current_user.id)
    
    if (remaining.Qty == 0) :
        return { "filledQuantity": order.quantity}

    if(order.order_type == "buy"):
        await set_redis_data(f"stock:{order.stock}:buy", remaining.price, remaining.Qty)
        # update the orders db
        return {"data": {
            "remaining_amount": remaining.price,
            "remaining_Qty": remaining.Qty, # remaning qty to buy
        }}
    else:
        await set_redis_data(f"stock:{order.stock}:buy", order.price, remaining.Qty)
        # update the orders db 
        return {"data": {
            "remaining_Qty": remaining.Qty, #remaning qty to sell
        }}
    
    
    