from pydantic import BaseModel

class TaskCreate(BaseModel):
    title:str
    description:str
    priority:str="medium"

class TaskUpdate(BaseModel):
    title:str
    description:str
    status:str="pending"
    priority:str="medium"