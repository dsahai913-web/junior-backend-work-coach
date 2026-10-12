
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from core.database import Base


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False,
        index=True
    )

    level = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),
    )