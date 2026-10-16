from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.tracker import Category
from app.models.user import User

def validate_references(session, data):
    if 'category_id' in data and session.get(Category,data['category_id']) is None:
        raise HTTPException(404,'Category not found')
    if data.get('assigned_user_id') is not None:
        user=session.get(User,data['assigned_user_id'])
        if user is None or user.deleted(): raise HTTPException(404,'Assigned user not found')


class SaveIssue:
    def __init__(self, session, issue):
        self.session = session
        self.issue = issue

    def execute(self):
        self.session.add(self.issue)
        try: self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(409,'Referenced record changed; refresh and try again') from None
        self.session.refresh(self.issue)
