from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Literal, List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://postgres:marvin123@localhost:5432/mini_trading_app"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT version();")
        for row in result:
            print(row)
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    instrument = Column(String, index=True)
    way = Column(String, index=True)
    price = Column(Float)
    qty = Column(Integer)
    is_executed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

Base.metadata.create_all(bind=engine)

class Order(BaseModel):
    instrument: str
    way: Literal['buy', 'sell']
    price: float
    qty: int
    is_executed: bool = False

class OrderResponse(Order):
    id: int
    created_at: datetime.datetime
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"Trade API": "Become a millionaire in your magical fantasy."}

@app.post("/orders")
def create_trade(trade: Order, db: Session = Depends(get_db)):
    if trade.way not in ['buy', 'sell']:
        raise HTTPException(status_code=400, detail="Invalid trade way. Use 'buy' or 'sell'.")
    if trade.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero.")
    if trade.qty <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero.")
    if trade.instrument == "":
        raise HTTPException(status_code=400, detail="Instrument cannot be empty.")
    
    db_order = OrderDB(**trade.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found.")
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order

@app.get("/orders/{order_id}/execute")
def execute_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    if order.is_executed:
        raise HTTPException(status_code=400, detail="Order already executed.")
    order.is_executed = True
    db.commit()
    return {"message": "Order executed successfully.", "order": order}


