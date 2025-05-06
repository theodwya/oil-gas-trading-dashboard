from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(".env")

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("SNOWFLAKE_DATABASE_URL")
engine = create_engine(DATABASE_URL)


class Trade(BaseModel):
    user_id: int
    commodity: str
    price: float
    volume: int
    trade_type: str


@app.get("/")
def read_root():
    return {"message": "Oil & Gas Trading Backend Running"}


@app.get("/marketdata/")
def get_market_data(commodity: str):
    query = text(
        "SELECT date, price, volume FROM MarketData WHERE commodity = :commodity ORDER BY date DESC LIMIT 10")
    with engine.connect() as conn:
        result = conn.execute(query, {"commodity": commodity})
        data = [{"date": r[0].strftime(
            "%Y-%m-%d"), "price": r[1], "volume": r[2]} for r in result]
    return data


@app.post("/trade/")
def submit_trade(trade: Trade):
    query = text("""
        INSERT INTO Trades (user_id, commodity, price, volume, trade_date, trade_type)
        VALUES (:user_id, :commodity, :price, :volume, CURRENT_DATE, :trade_type)
    """)
    with engine.connect() as conn:
        conn.execute(query, trade.dict())
    return {"message": "Trade submitted"}
