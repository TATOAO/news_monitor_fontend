from sqlmodel import Field, SQLModel, Relationship, JSON
from typing import Optional, List, Dict, Any, TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from .news import News
    from .user import User

class Analysis(SQLModel, table=True):
    __tablename__ = "analyses"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    news_id: int = Field(foreign_key="news.id", unique=True)
    sentiment_score: float  # Range from -1.0 (negative) to 1.0 (positive)
    confidence: float  # Range from 0.0 to 1.0
    entities: Optional[str] = Field(default=None, sa_column=JSON)  # Extracted entities (people, organizations, etc.)
    keywords: Optional[str] = Field(default=None, sa_column=JSON)  # Key terms extracted from the article
    summary: Optional[str] = None  # AI-generated summary
    model_version: str = Field(max_length=50)  # Version of the AI model used
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, sa_column_kwargs={"onupdate": datetime.datetime.utcnow})
    
    # Relationships
    news: "News" = Relationship(back_populates="analysis")
    annotations: List["Annotation"] = Relationship(back_populates="analysis", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Annotation(SQLModel, table=True):
    __tablename__ = "annotations"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    analysis_id: int = Field(foreign_key="analyses.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    text: str
    override_sentiment: Optional[float] = None  # If analyst wants to override the AI sentiment
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    
    # Relationships
    analysis: Analysis = Relationship(back_populates="annotations")
    user: Optional["User"] = Relationship() 