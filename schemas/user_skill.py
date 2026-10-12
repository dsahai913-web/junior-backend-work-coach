
from pydantic import BaseModel, Field


class UserSkillCreate(BaseModel):
    skill_id: int
    level: int = Field(default=1, ge=1, le=5)


class UserSkillUpdate(BaseModel):
    level: int = Field(ge=1, le=5)


class UserSkillResponse(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    level: int