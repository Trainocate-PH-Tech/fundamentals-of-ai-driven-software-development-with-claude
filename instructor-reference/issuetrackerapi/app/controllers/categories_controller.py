from app.operations.tracker.save_category import SaveCategory
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies.auth import require_active_user
from app.models.tracker import Category, Issue
from app.schemas.tracker import CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(require_active_user)])


def category_dict(category):
    return {key: getattr(category, key) for key in ["id", "name", "description", "created_at", "updated_at"]}


def find_category(session, category_id):
    category = session.get(Category, category_id)
    if category is None:
        raise HTTPException(404, "Category not found")
    return category


def save_category(session, category):
    command = SaveCategory(session, category)
    command.execute()
    return category_dict(command.category)


@router.get("")
def index(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100), session: Session = Depends(get_db)):
    total = session.scalar(select(func.count()).select_from(Category))
    pages = max(1, (total + per_page - 1) // per_page)
    records = session.scalars(select(Category).order_by(func.lower(Category.name), Category.id).offset((page-1)*per_page).limit(per_page)).all()
    return {"records": [category_dict(c) for c in records], "current_page": page, "total_pages": pages,
            "next_page": page+1 if page < pages else None, "prev_page": page-1 if page > 1 else None}


@router.post("", status_code=201)
def create(payload: CategoryCreate, session: Session = Depends(get_db)):
    return save_category(session, Category(**payload.model_dump()))


@router.get("/{category_id}")
def show(category_id: str, session: Session = Depends(get_db)):
    return category_dict(find_category(session, category_id))


@router.patch("/{category_id}")
def update(category_id: str, payload: CategoryUpdate, session: Session = Depends(get_db)):
    category = find_category(session, category_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    return save_category(session, category)


@router.delete("/{category_id}", status_code=204)
def delete(category_id: str, session: Session = Depends(get_db)):
    category = find_category(session, category_id)
    if session.scalar(select(Issue.id).where(Issue.category_id == category_id).limit(1)):
        raise HTTPException(409, "Category is used by issues and cannot be deleted")
    session.delete(category)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(409, "Category is used by issues and cannot be deleted") from None
    return Response(status_code=204)
