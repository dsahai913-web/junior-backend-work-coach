import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.database import SessionLocal
from models.task import Task
from models.user import User
from models.user_skill import UserSkill
from models.skill import Skill
from schemas.task import TaskCreate, TaskUpdate
from AI.analyzer import analyze_task


def create_task(
        db: Session,
        current_user: User,
        task_data: TaskCreate,
        idempotency_key: str
):
    existing_task = db.query(Task).filter(
        Task.idempotency_key == idempotency_key,
        Task.user_id == current_user.id
    ).first()

    if existing_task is not None:
        return existing_task

    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        ai_explanation=None,
        ai_status="pending",
        priority=task_data.priority,
        idempotency_key=idempotency_key,
    )

    db.add(new_task)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        existing_task = db.query(Task).filter(
            Task.idempotency_key == idempotency_key
        ).first()

        if existing_task is not None:
            return existing_task

        raise

    db.refresh(new_task)

    return new_task


def get_user_task(
        db: Session,
        task_id: int,
        current_user: User
):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()


def get_user_tasks(
        db: Session,
        current_user: User
):
    return db.query(Task).filter(
        Task.user_id == current_user.id
    ).all()


def update_user_task(
        db: Session,
        task_id: int,
        current_user: User,
        task_data: TaskUpdate
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    description_changed = (
        task.description != task_data.description
    )

    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.priority = task_data.priority

    if description_changed:
        task.ai_explanation = None
        task.ai_status = "pending"

    db.commit()
    db.refresh(task)

    return task, description_changed


def delete_user_task(
        db: Session,
        task_id: int,
        current_user: User
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return task



def analyze_task_in_background(task_id: int):
    db = SessionLocal()

    try:
        task = db.query(Task).filter(
            Task.id == task_id
        ).first()

        if task is None:
            return

        task.ai_status = "pending"
        db.commit()

        print(f"STARTING AI ANALYSIS FOR TASK {task_id}")

        # Fetch only the skills belonging to this task's owner.
        saved_skills = (
            db.query(Skill.name, UserSkill.level)
            .join(
                UserSkill,
                UserSkill.skill_id == Skill.id
            )
            .filter(
                UserSkill.user_id == task.user_id
            )
            .all()
        )

        user_skills = [
            {
                "skill": skill_name,
                "level": level
            }
            for skill_name, level in saved_skills
        ]

        print(
            f"Found {len(user_skills)} saved skills "
            f"for task {task_id}"
        )

        # Pass the user's skills to the updated AI analyzer.
        ai_result = analyze_task(
            task.description,
            user_skills
        )

        print(f"AI ANALYSIS COMPLETED FOR TASK {task_id}")

        task = db.query(Task).filter(
            Task.id == task_id
        ).first()

        if task is None:
            return

        task.ai_explanation = json.dumps(
            ai_result,
            ensure_ascii=False
        )

        task.ai_status = "completed"
        db.commit()

    except Exception as e:
        db.rollback()

        print(
            f"Background AI analysis failed for task "
            f"{task_id}: {e}"
        )

        try:
            task = db.query(Task).filter(
                Task.id == task_id
            ).first()

            if task is not None:
                task.ai_status = "failed"
                db.commit()

        except Exception as status_error:
            db.rollback()
            print(
                f"Could not save failed status for task "
                f"{task_id}: {status_error}"
            )

    finally:
        db.close()


def retry_task_analysis(
        db: Session,
        task_id: int,
        current_user: User
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.ai_explanation = None
    task.ai_status = "pending"

    db.commit()

    return task