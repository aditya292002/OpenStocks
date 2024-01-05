from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.responses import HTMLResponse
from .database import engine
from . import models
from .router import order_book, auth, place_order, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # Consider using Alembic for production
app.include_router(order_book.router)
app.include_router(auth.router)
app.include_router(place_order.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "hello world"}