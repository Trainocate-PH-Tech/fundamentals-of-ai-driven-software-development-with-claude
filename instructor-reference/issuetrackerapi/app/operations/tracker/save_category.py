from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from app.models.tracker import Category

class SaveCategory:
    def __init__(self, session, category):
        self.session = session
        self.category = category

    def execute(self):
        duplicate = self.session.scalar(select(Category.id).where(
            func.lower(Category.name) == self.category.name.lower(), Category.id != self.category.id
        )) if self.category.id else self.session.scalar(select(Category.id).where(func.lower(Category.name) == self.category.name.lower()))
        if duplicate:
            raise HTTPException(409, "Category name already exists")
        self.session.add(self.category)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(409, "Category name already exists") from None
        self.session.refresh(self.category)
