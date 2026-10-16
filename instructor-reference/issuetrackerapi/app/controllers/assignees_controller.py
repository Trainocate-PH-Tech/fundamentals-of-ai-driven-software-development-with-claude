from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies.auth import require_active_user
from app.models.user import User

router=APIRouter(prefix='/assignees',tags=['assignees'],dependencies=[Depends(require_active_user)])


@router.get('')
def index(session:Session=Depends(get_db)):
    users=session.scalars(select(User).where(User.status!='deleted').order_by(User.last_name,User.first_name,User.id)).all()
    return [{'id':user.id,'full_name':user.full_name()} for user in users]
