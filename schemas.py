from pydantic import BaseModel
from typing import Optional

class MoodRequest(BaseModel):
    mood: str        
    language: str    

class MoodResponse(BaseModel):
    mood_detected: str
    content: str     
    author_or_poet: Optional[str] = "System"