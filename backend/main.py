from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    instrument: str
    way: Literal['buy', 'sell']
    price: float
    qty: int
    is_executed: bool = False

orders = []

@app.get("/")
def root():
    return {"Trade API": "Become a millionaire in your magical fantasy."}

@app.post("/orders")
def create_trade(trade: Order):
    if trade.way not in ['buy', 'sell']:
        raise HTTPException(status_code=400, detail="Invalid trade way. Use 'buy' or 'sell'.")
    if trade.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero.")
    if trade.qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    if trade.instrument == "":
        raise HTTPException(status_code=400, detail="Instrument cannot be empty.")
    orders.append(trade)
    return "Successful sent order!"

@app.get("/orders", response_model=list[Order])
def get_orders():
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found.")
    return orders

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    if order_id < 0 or order_id >= len(orders):
        raise HTTPException(status_code=404, detail="Order not found.")
    return orders[order_id]

@app.get("/orders/{order_id}/execute")
def execute_order(order_id: int):
    if order_id < 0 or order_id >= len(orders):
        raise HTTPException(status_code=404, detail="Order not found.")
    order = orders[order_id]
    if order.is_executed:
        raise HTTPException(status_code=400, detail="Order already executed.")
    order.is_executed = True
    return {"message": "Order executed successfully.", "order": order}


