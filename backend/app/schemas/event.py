from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class InteractionEventSchema(BaseModel):
    event_id: Optional[str] = None
    user_id: str
    event_type: str  # e.g., 'quiz_submitted', 'lesson_watched', 'course_enrolled'
    timestamp: Optional[datetime] = None
    lesson_id: Optional[str] = None
    course_id: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
