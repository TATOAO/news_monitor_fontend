from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import date

from ....core.database import get_session
from ....core.security import get_current_user
from ....models.user import User
from ....models.news import NewsItem
from ....schemas.news import NewsCreate, NewsResponse, NewsUpdate

router = APIRouter()

@router.get("/", response_model=List[NewsResponse])
def get_news_items(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    keyword: Optional[str] = None,
    asset_symbol: Optional[str] = None,
    sentiment: Optional[float] = None
) -> Any:
    """
    Retrieve news items with optional filtering.
    """
    query = select(NewsItem)
    
    # Apply filters if provided
    if start_date:
        query = query.filter(NewsItem.published_date >= start_date)
    if end_date:
        query = query.filter(NewsItem.published_date <= end_date)
    if keyword:
        query = query.filter(NewsItem.headline.contains(keyword) | NewsItem.content.contains(keyword))
    if asset_symbol:
        # This assumes you have a relationship between news and assets
        # You might need to adjust this based on your actual model structure
        query = query.filter(NewsItem.assets.any(symbol=asset_symbol))
    if sentiment is not None:
        # This assumes you have a sentiment field in your news model
        # You might need to adjust this based on your actual model structure
        query = query.filter(NewsItem.sentiment == sentiment)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    news_items = session.exec(query).all()
    return news_items

@router.get("/{news_id}", response_model=NewsResponse)
def get_news_item(
    *,
    news_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific news item by id.
    """
    news_item = session.get(NewsItem, news_id)
    if not news_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News item not found"
        )
    
    return news_item

@router.post("/", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
def create_news_item(
    *,
    news_in: NewsCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new news item.
    """
    # Check if user has permission to create news items
    if not current_user.is_admin and not current_user.can_create_news:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create new news item
    news_item = NewsItem.from_schema(news_in)
    news_item.created_by_id = current_user.id
    
    session.add(news_item)
    session.commit()
    session.refresh(news_item)
    
    return news_item

@router.put("/{news_id}", response_model=NewsResponse)
def update_news_item(
    *,
    news_id: int,
    news_in: NewsUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a news item.
    """
    news_item = session.get(NewsItem, news_id)
    if not news_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News item not found"
        )
    
    # Check if user has permission to update this news item
    if not current_user.is_admin and news_item.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update news item attributes
    news_data = news_in.dict(exclude_unset=True)
    for key, value in news_data.items():
        setattr(news_item, key, value)
    
    news_item.updated_by_id = current_user.id
    
    session.add(news_item)
    session.commit()
    session.refresh(news_item)
    
    return news_item

@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news_item(
    *,
    news_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete a news item.
    """
    news_item = session.get(NewsItem, news_id)
    if not news_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News item not found"
        )
    
    # Check if user has permission to delete this news item
    if not current_user.is_admin and news_item.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    session.delete(news_item)
    session.commit()

@router.post("/{news_id}/reanalyze", response_model=NewsResponse)
def reanalyze_news_item(
    *,
    news_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Trigger re-analysis of a news item.
    """
    news_item = session.get(NewsItem, news_id)
    if not news_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News item not found"
        )
    
    # Here you would trigger your AI pipeline to re-analyze the news item
    # This is a placeholder for the actual implementation
    
    # For example, you might set a flag to indicate that re-analysis is needed
    news_item.needs_reanalysis = True
    session.add(news_item)
    session.commit()
    session.refresh(news_item)
    
    return news_item 