import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True, nullable=True)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=True)
    currency = Column(String, default="USD")
    
    # Store dynamic lists and dicts as JSON strings in SQLite
    features = Column(Text, nullable=True)  # JSON list
    specifications = Column(Text, nullable=True)  # JSON dict
    target_audience = Column(String, nullable=True)
    primary_keywords = Column(Text, nullable=True)  # JSON list
    secondary_keywords = Column(Text, nullable=True)  # JSON list
    usp = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    material = Column(String, nullable=True)
    dimensions = Column(String, nullable=True)
    color = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    generated_contents = relationship("GeneratedContent", back_populates="product", cascade="all, delete-orphan")
