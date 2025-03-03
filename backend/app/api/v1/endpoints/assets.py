from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Any, List, Optional
from datetime import date, datetime

from ....core.database import get_session
from ....core.security import get_current_user
from ....models.user import User
from ....models.asset import Asset, AssetPrice
from ....schemas.asset import AssetCreate, AssetResponse, AssetUpdate, AssetPriceResponse

router = APIRouter()

@router.get("/", response_model=List[AssetResponse])
def get_assets(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    asset_type: Optional[str] = None,
    sector: Optional[str] = None,
    region: Optional[str] = None
) -> Any:
    """
    Retrieve assets with optional filtering.
    """
    query = select(Asset)
    
    # Apply filters if provided
    if asset_type:
        query = query.filter(Asset.asset_type == asset_type)
    if sector:
        query = query.filter(Asset.sector == sector)
    if region:
        query = query.filter(Asset.region == region)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    assets = session.exec(query).all()
    return assets

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    *,
    asset_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific asset by id.
    """
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    return asset

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    *,
    asset_in: AssetCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new asset.
    """
    # Check if user has permission to create assets
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if asset with given symbol already exists
    existing_asset = session.query(Asset).filter(Asset.symbol == asset_in.symbol).first()
    if existing_asset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An asset with this symbol already exists"
        )
    
    # Create new asset
    asset = Asset.from_schema(asset_in)
    
    session.add(asset)
    session.commit()
    session.refresh(asset)
    
    return asset

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    *,
    asset_id: int,
    asset_in: AssetUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update an asset.
    """
    # Check if user has permission to update assets
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    # Update asset attributes
    asset_data = asset_in.dict(exclude_unset=True)
    for key, value in asset_data.items():
        setattr(asset, key, value)
    
    session.add(asset)
    session.commit()
    session.refresh(asset)
    
    return asset

@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    *,
    asset_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete an asset.
    """
    # Check if user has permission to delete assets
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    session.delete(asset)
    session.commit()

@router.get("/{asset_id}/prices", response_model=List[AssetPriceResponse])
def get_asset_prices(
    *,
    asset_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    interval: Optional[str] = "1d"  # Options: 1m, 1h, 1d
) -> Any:
    """
    Get historical price data for an asset.
    """
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    query = select(AssetPrice).where(AssetPrice.asset_id == asset_id)
    
    # Apply date range filters if provided
    if start_date:
        query = query.filter(AssetPrice.timestamp >= start_date)
    if end_date:
        query = query.filter(AssetPrice.timestamp <= end_date)
    
    # Apply interval filter (this is a simplified implementation)
    # In a real application, you might have different tables for different intervals
    # or a more sophisticated way to handle this
    if interval == "1m":
        # Return minute-by-minute data
        pass
    elif interval == "1h":
        # Return hourly data
        pass
    elif interval == "1d":
        # Return daily data
        pass
    
    # Order by timestamp
    query = query.order_by(AssetPrice.timestamp)
    
    prices = session.exec(query).all()
    return prices 