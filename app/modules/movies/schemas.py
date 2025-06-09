from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[int] = None
    genre_ids: Optional[List[int]] = []

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class MovieOut(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
