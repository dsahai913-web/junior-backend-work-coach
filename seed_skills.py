
from core.database import SessionLocal
from models.skill import Skill


DEFAULT_SKILLS = [
    "Python",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "React",
    "FastAPI",
    "Django",
    "Node.js",
    "Express.js",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "SQLAlchemy",
    "Git",
    "Docker",
    "REST API",
    "Redis",
    "AWS",
    "Problem Solving",
]


def seed_skills():
    db = SessionLocal()

    try:
        for skill_name in DEFAULT_SKILLS:
            existing_skill = (
                db.query(Skill)
                .filter(Skill.name == skill_name)
                .first()
            )

            if existing_skill is None:
                db.add(Skill(name=skill_name))

        db.commit()
        print("Skills seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_skills()

