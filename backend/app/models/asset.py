from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
import datetime
import enum

if TYPE_CHECKING:
    from .news import AssetMention

class AssetType(str, enum.Enum):
    STOCK = "stock"
    FOREX = "forex"
    CRYPTO = "crypto"
    COMMODITY = "commodity"
    INDEX = "index"
    OTHER = "other"

class Asset(SQLModel, table=True):
    __tablename__ = "assets"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    symbol: str = Field(max_length=20, unique=True, index=True)
    name: str = Field(max_length=255)
    description: Optional[str] = None
    asset_type: AssetType = Field(default=AssetType.STOCK)
    sector: Optional[str] = Field(default=None, max_length=100)
    region: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, sa_column_kwargs={"onupdate": datetime.datetime.utcnow})
    
    # Relationships
    news_mentions: List["AssetMention"] = Relationship(back_populates="asset", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    price_history: List["AssetPrice"] = Relationship(back_populates="asset", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class AssetPrice(SQLModel, table=True):
    __tablename__ = "asset_prices"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    asset_id: int = Field(foreign_key="assets.id")
    timestamp: datetime.datetime = Field(index=True)
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: Optional[float] = None
    
    # Relationships
    asset: Asset = Relationship(back_populates="price_history") 