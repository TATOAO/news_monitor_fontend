from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import date, datetime
from pydantic import BaseModel

from ....core.database import get_session
from ....core.security import get_current_user
from ....models.user import User
from ....models.news import NewsItem, NewsEvent
from ....schemas.news import NewsCreate, NewsResponse, NewsUpdate

router = APIRouter()

class NewsEvent(BaseModel):
    date: str
    title: str
    content: str
    entities: List[str]
    relation: str

# Demo data from example_data.md
DEMO_NEWS_EVENTS = [
    {"date": "2024-05-07", "title": "A国央行宣布启动数字货币研究项目", "content": "A国财政部长表示将在6个月内完成技术验证...", "entities": ["A国央行", "数字货币"], "relation": "事件起点"},
    {"date": "2024-05-11", "title": "国际清算银行警告数字货币风险", "content": "BIS报告指出A国方案可能影响跨境支付体系...", "entities": ["BIS"], "relation": "外部压力"},
    {"date": "2024-05-16", "title": "A国公布数字法币技术白皮书", "content": "采用混合区块链架构，保留央行控制权...", "entities": ["区块链"], "relation": "技术演进"},
    {"date": "2024-05-21", "title": "跨国银行联盟宣布兼容A国标准", "content": "JP摩根、汇丰等20家机构签署技术协议...", "entities": ["JP摩根", "汇丰"], "relation": "生态扩展"},
    {"date": "2024-05-24", "title": "A国数字货币试点现技术漏洞", "content": "压力测试中发现双花攻击漏洞...", "entities": [], "relation": "风险事件"},
    {"date": "2024-05-26", "title": "央行紧急升级智能合约模块", "content": "引入零知识证明强化隐私保护...", "entities": ["智能合约"], "relation": "技术迭代"},
    {"date": "2024-05-28", "title": "国际货币基金组织表态支持", "content": "IMF认为有助于提升金融监管效率...", "entities": ["IMF"], "relation": "政策背书"},
    {"date": "2024-05-31", "title": "反对党质疑项目透明度", "content": "国会听证会要求公开技术审计报告...", "entities": ["国会"], "relation": "政治阻力"},
    {"date": "2024-06-02", "title": "央行数字法币首次跨境结算测试成功", "content": "与C国完成1亿美元实时转账...", "entities": ["C国"], "relation": "里程碑"},
    {"date": "2024-06-05", "title": "A国宣布正式发行数字法币", "content": "第一阶段覆盖大额机构交易...", "entities": [], "relation": "成果落地"}
]

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

@router.get("/news/events", response_model=List[NewsEvent])
async def get_news_events():
    """
    Get all news events with their details (Demo data)
    """
    return DEMO_NEWS_EVENTS

@router.get("/news/events/{event_id}", response_model=NewsEvent)
async def get_news_event(event_id: int):
    """
    Get a specific news event by ID (Demo data)
    """
    if event_id < 0 or event_id >= len(DEMO_NEWS_EVENTS):
        raise HTTPException(status_code=404, detail="Event not found")
    return DEMO_NEWS_EVENTS[event_id] 