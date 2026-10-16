"""Idempotent sample categories, independent of user seeding."""
from sqlalchemy import func, select
from app.models.tracker import Category


def seed_categories(session):
    for name in ["Bug", "Feature Request", "Task", "Documentation"]:
        if not session.scalar(select(Category).where(func.lower(Category.name) == name.lower())):
            session.add(Category(name=name))
    session.commit()


if __name__ == "__main__":
    from app import create_app
    from app.db import db
    create_app()
    with db.session() as session:
        seed_categories(session)
    print("Sample categories ready.")
