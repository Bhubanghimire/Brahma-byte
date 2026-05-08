from pydantic import BaseModel
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    message: str

class NotificationResponse(BaseModel):
    id: int
    user_id: str
    message: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }