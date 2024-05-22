from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ImageRead(BaseModel):
    id: UUID
    name: str
    image_url: str
    created_at: Optional[datetime] = None
