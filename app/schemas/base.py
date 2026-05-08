from pydantic import BaseModel
from typing import Any, Optional

class ApiResponse(BaseModel):
    data: Any = None
    message: str