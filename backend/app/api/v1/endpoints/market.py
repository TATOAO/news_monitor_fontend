from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class MarketData(BaseModel):
    date: str
    open: float
    close: float
    high: float
    low: float
    volume: float

# Demo data from example_data.md
DEMO_MARKET_DATA = [
    {"date": "2024-05-07", "open": 3250, "close": 3265, "high": 3280, "low": 3240, "volume": 150},
    {"date": "2024-05-08", "open": 3265, "close": 3270, "high": 3285, "low": 3250, "volume": 140},
    {"date": "2024-05-09", "open": 3270, "close": 3260, "high": 3290, "low": 3255, "volume": 130},
    {"date": "2024-05-10", "open": 3260, "close": 3255, "high": 3275, "low": 3245, "volume": 120},
    {"date": "2024-05-11", "open": 3280, "close": 3200, "high": 3285, "low": 3180, "volume": 450},
    {"date": "2024-05-12", "open": 3200, "close": 3210, "high": 3220, "low": 3190, "volume": 160},
    {"date": "2024-05-13", "open": 3210, "close": 3220, "high": 3230, "low": 3200, "volume": 170},
    {"date": "2024-05-14", "open": 3220, "close": 3230, "high": 3240, "low": 3210, "volume": 180},
    {"date": "2024-05-15", "open": 3230, "close": 3240, "high": 3250, "low": 3220, "volume": 190},
    {"date": "2024-05-16", "open": 3220, "close": 3300, "high": 3320, "low": 3205, "volume": 380},
    {"date": "2024-05-17", "open": 3300, "close": 3310, "high": 3320, "low": 3290, "volume": 200},
    {"date": "2024-05-18", "open": 3310, "close": 3320, "high": 3330, "low": 3300, "volume": 210},
    {"date": "2024-05-19", "open": 3320, "close": 3330, "high": 3340, "low": 3310, "volume": 220},
    {"date": "2024-05-20", "open": 3330, "close": 3340, "high": 3350, "low": 3320, "volume": 230},
    {"date": "2024-05-21", "open": 3350, "close": 3400, "high": 3420, "low": 3340, "volume": 420},
    {"date": "2024-05-22", "open": 3400, "close": 3410, "high": 3420, "low": 3390, "volume": 240},
    {"date": "2024-05-23", "open": 3410, "close": 3420, "high": 3430, "low": 3400, "volume": 250},
    {"date": "2024-05-24", "open": 3420, "close": 3330, "high": 3425, "low": 3300, "volume": 600},
    {"date": "2024-05-25", "open": 3330, "close": 3320, "high": 3340, "low": 3310, "volume": 260},
    {"date": "2024-05-26", "open": 3320, "close": 3380, "high": 3400, "low": 3300, "volume": 520},
    {"date": "2024-05-27", "open": 3380, "close": 3400, "high": 3410, "low": 3370, "volume": 270},
    {"date": "2024-05-28", "open": 3400, "close": 3450, "high": 3460, "low": 3390, "volume": 400},
    {"date": "2024-05-29", "open": 3450, "close": 3460, "high": 3470, "low": 3440, "volume": 280},
    {"date": "2024-05-30", "open": 3460, "close": 3420, "high": 3465, "low": 3400, "volume": 480},
    {"date": "2024-05-31", "open": 3420, "close": 3430, "high": 3440, "low": 3410, "volume": 290},
    {"date": "2024-06-01", "open": 3430, "close": 3440, "high": 3450, "low": 3420, "volume": 300},
    {"date": "2024-06-02", "open": 3430, "close": 3500, "high": 3520, "low": 3420, "volume": 650},
    {"date": "2024-06-03", "open": 3500, "close": 3510, "high": 3520, "low": 3490, "volume": 310},
    {"date": "2024-06-04", "open": 3510, "close": 3520, "high": 3530, "low": 3500, "volume": 320},
    {"date": "2024-06-05", "open": 3520, "close": 3600, "high": 3620, "low": 3510, "volume": 800}
]

@router.get("/market/data", response_model=List[MarketData])
async def get_market_data():
    """
    Get all market data points (Demo data)
    """
    return DEMO_MARKET_DATA

@router.get("/market/data/{date}", response_model=List[MarketData])
async def get_market_data_by_date(date: str):
    """
    Get market data for a specific date (Demo data)
    """
    matching_data = [data for data in DEMO_MARKET_DATA if data["date"] == date]
    if not matching_data:
        raise HTTPException(status_code=404, detail="Market data not found for this date")
    return matching_data 