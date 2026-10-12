from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import engine
from models.user import User
from models.user_skill import UserSkill
from schemas.user_skill import UserSkillCreate
from schemas.user_skill import UserSkillUpdate

from routers.user import router as user_router
from routers.task import router as task_router
from routers.user_skill import router as user_skill_router

from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI(title="Working")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(task_router)
app.include_router(user_skill_router)


@app.get("/")
def home():
    return {
        "message": "Hello World"
    }