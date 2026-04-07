from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date
from enum import Enum

class ActionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class ActionItem(BaseModel):
    description: str = Field(..., min_length=5, max_length=500)
    owner: str = Field(..., min_length=1, max_length=100)
    deadline: Optional[date] = Field(None)
    status: ActionStatus = Field(default=ActionStatus.PENDING)
    id: Optional[int] = Field(None)

class Transcript(BaseModel):
    content: str = Field(..., max_length=10000)
    ground_truth: List[ActionItem] = Field(..., min_length=1)
    task_id: str = Field(..., pattern=r'^task_\d+$')
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentAction(BaseModel):
    action_type: str = Field(..., pattern=r'^(extract_action|assign_owner|set_deadline|mark_complete)$')
    value: Optional[str] = Field(None)

class EnvState(BaseModel):
    current_actions: List[ActionItem] = Field(default_factory=list)
    transcript: Transcript = Field(...)
    step_count: int = Field(default=0, ge=0)
    total_reward: float = Field(default=0.0)

class RewardEvent(BaseModel):
    action: AgentAction
    reward: float
    message: str
    state: EnvState