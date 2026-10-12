
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.skill import Skill
from models.user_skill import UserSkill
from schemas.user_skill import (
    UserSkillCreate,
    UserSkillUpdate,
    UserSkillResponse,
)

router = APIRouter(
    prefix="/users/me/skills",
    tags=["user skills"],
)

@router.post("/", response_model=UserSkillResponse, status_code=201)
def add_user_skill(
    skill_data: UserSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = (
        db.query(Skill)
        .filter(Skill.id == skill_data.skill_id)
        .first()
    )

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    existing_user_skill = (
        db.query(UserSkill)
        .filter(
            UserSkill.user_id == current_user.id,
            UserSkill.skill_id == skill_data.skill_id,
        )
        .first()
    )

    if existing_user_skill:
        raise HTTPException(
            status_code=409,
            detail="You have already added this skill",
        )

    user_skill = UserSkill(
        user_id=current_user.id,
        skill_id=skill.id,
        level=skill_data.level,
    )

    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    return {
        "id": user_skill.id,
        "skill_id": skill.id,
        "skill_name": skill.name,
        "level": user_skill.level,
    }


@router.get("/", response_model=list[UserSkillResponse])
def get_my_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_skills = (
        db.query(UserSkill, Skill)
        .join(Skill, UserSkill.skill_id == Skill.id)
        .filter(UserSkill.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": user_skill.id,
            "skill_id": skill.id,
            "skill_name": skill.name,
            "level": user_skill.level,
        }
        for user_skill, skill in user_skills
    ]


@router.patch("/{user_skill_id}", response_model=UserSkillResponse)
def update_user_skill(
    user_skill_id: int,
    skill_data: UserSkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_skill = (
        db.query(UserSkill)
        .filter(
            UserSkill.id == user_skill_id,
            UserSkill.user_id == current_user.id,
        )
        .first()
    )

    if user_skill is None:
        raise HTTPException(
            status_code=404,
            detail="User skill not found",
        )

    user_skill.level = skill_data.level

    db.commit()
    db.refresh(user_skill)

    skill = (
        db.query(Skill)
        .filter(Skill.id == user_skill.skill_id)
        .first()
    )

    return {
        "id": user_skill.id,
        "skill_id": skill.id,
        "skill_name": skill.name,
        "level": user_skill.level,
    }


@router.delete("/{user_skill_id}", status_code=204)
def delete_user_skill(
    user_skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_skill = (
        db.query(UserSkill)
        .filter(
            UserSkill.id == user_skill_id,
            UserSkill.user_id == current_user.id,
        )
        .first()
    )

    if user_skill is None:
        raise HTTPException(
            status_code=404,
            detail="User skill not found",
        )

    db.delete(user_skill)
    db.commit()

    return None


@router.get("/available")
def get_available_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = (
        db.query(Skill)
        .order_by(Skill.name)
        .all()
    )

    return [
        {
            "id": skill.id,
            "name": skill.name,
        }
        for skill in skills
    ]










