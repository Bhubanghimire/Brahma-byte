from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True