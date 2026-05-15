from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#автоматически проверяют входящие данные
class Task(BaseModel): #каждая задача должна выглядеть так
    title: str = Field(..., min_length=1, max_length=100) #обязателен текст
    description: Optional[str] = None # может быть пустым
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    completed: bool = False
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None #может быть, а может нет 
    description: Optional[str] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None