from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Column, Integer
import datetime

if TYPE_CHECKING:
    from .analysis import Analysis
    from .asset import Asset

class NewsItem(SQLModel, table=True):
    __tablename__ = "news"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(max_length=255, index=True)
    content: str
    summary: Optional[str] = None
    source: str = Field(max_length=255)
    url: Optional[str] = Field(default=None, max_length=512)
    published_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.datetime.utcnow}
    )
    
    # Relationships
    analysis: Optional["Analysis"] = Relationship(back_populates="news", sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"})
    asset_mentions: List["AssetMention"] = Relationship(back_populates="news", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class AssetMention(SQLModel, table=True):
    __tablename__ = "asset_mentions"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    news_id: int = Field(
        foreign_key="news.id",
    )
    asset_id: int = Field(
        foreign_key="assets.id",
    )
    mention_count: int = Field(default=1)
    
    # Relationships
    news: NewsItem = Relationship(back_populates="asset_mentions")
    asset: "Asset" = Relationship(back_populates="news_mentions")