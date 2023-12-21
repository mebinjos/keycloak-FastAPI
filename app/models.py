from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    keycloak_id = Column(String, unique=True, index=True)  # Unique ID from Keycloak
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)  # To keep track of the email
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), onupdate=func.now())

# Additional models and relationships can be added as required
