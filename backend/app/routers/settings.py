from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import SettingsRepository
from app.schemas.brand_settings import BrandSettingsBase, BrandSettingsUpdate, BrandSettingsResponse

router = APIRouter(prefix="/api/settings/brand", tags=["Brand Settings"])

@router.get("", response_model=BrandSettingsBase)
def get_brand_settings(db: Session = Depends(get_db)):
    settings = SettingsRepository.get_settings(db)
    return SettingsRepository.to_schema(settings)

@router.put("", response_model=BrandSettingsBase)
def update_brand_settings(settings_in: BrandSettingsUpdate, db: Session = Depends(get_db)):
    updated = SettingsRepository.update_settings(db, settings_in)
    return SettingsRepository.to_schema(updated)

@router.post("/reset", response_model=BrandSettingsBase)
def reset_brand_settings(db: Session = Depends(get_db)):
    reset_settings = SettingsRepository.reset_to_defaults(db)
    return SettingsRepository.to_schema(reset_settings)
