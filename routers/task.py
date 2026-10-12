from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from schemas.task import TaskCreate, TaskUpdate

from services.task_service import (
    create_task,
    get_user_task,
    get_user_tasks,
    update_user_task,
    delete_user_task,
    analyze_task_in_background,
    retry_task_analysis,
)


router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)


@router.post("")
def create_new_task(
        task_data: TaskCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
        idempotency_key: str = Header(...)
):
    new_task = create_task(
        db,
        current_user,
        task_data,
        idempotency_key
    )

    background_tasks.add_task(
        analyze_task_in_background,
        new_task.id
    )

    return {
        "message": "Task created successfully",
        "task": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "ai_explanation": new_task.ai_explanation,
        "ai_status": new_task.ai_status,
        "priority": new_task.priority,
        "user_id": new_task.user_id
    }


@router.get("")
def get_my_tasks(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    tasks = get_user_tasks(
        db,
        current_user
    )

    return tasks


@router.get("/{task_id}")
def get_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = get_user_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "ai_explanation": task.ai_explanation,
        "ai_status": task.ai_status,
        "status": task.status,
        "priority": task.priority,
        "user_id": task.user_id
    }


@router.put("/{task_id}")
def update_task(
        task_id: int,
        task_data: TaskUpdate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task, description_changed = update_user_task(
        db,
        task_id,
        current_user,
        task_data
    )

    if description_changed:
        background_tasks.add_task(
            analyze_task_in_background,
            task.id
        )

    return {
        "message": "Task updated successfully",
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "ai_explanation": task.ai_explanation,
        "ai_status": task.ai_status,
        "priority": task.priority,
        "status": task.status
    }


@router.post("/{task_id}/retry-ai")
def retry_ai_analysis(
        task_id: int,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = retry_task_analysis(
        db,
        task_id,
        current_user
    )

    background_tasks.add_task(
        analyze_task_in_background,
        task.id
    )

    return {
        "message": "AI analysis restarted",
        "task_id": task.id,
        "ai_status": task.ai_status
    }

@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    task = delete_user_task(
        db,
        task_id,
        current_user
    )

    return {
        "message": "Task deleted successfully",
        "task_id": task.id
    }