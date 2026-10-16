from app.operations.tracker.save_issue import SaveIssue, validate_references
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db import get_db
from app.dependencies.auth import require_active_user
from app.models.tracker import Category, Issue
from app.models.user import User
from app.schemas.tracker import IssueCreate, IssueUpdate, Status, Priority

router = APIRouter(prefix="/issues", tags=["issues"], dependencies=[Depends(require_active_user)])


def issue_dict(issue):
    result = {key: getattr(issue,key) for key in ['id','title','description','status','priority','category_id','assigned_user_id','created_at','updated_at']}
    result['category'] = {'id':issue.category.id,'name':issue.category.name}
    result['assigned_user'] = {'id':issue.assigned_user.id,'full_name':issue.assigned_user.full_name()} if issue.assigned_user else None
    return result


def find_issue(session, issue_id):
    issue=session.get(Issue,issue_id)
    if issue is None: raise HTTPException(404,'Issue not found')
    return issue


def save_issue(session, issue):
    command = SaveIssue(session, issue)
    command.execute()
    return issue_dict(command.issue)


@router.get('')
def index(page: int = Query(1,ge=1),per_page: int = Query(20,ge=1,le=100),
          search: str | None = None,status: Status | None = None,priority: Priority | None = None,
          category_id: str | None = None,assigned_user_id: str | None = None,
          session: Session=Depends(get_db)):
    stmt=select(Issue)
    if search:
        escaped=search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        stmt=stmt.where(Issue.title.ilike(f"%{escaped}%",escape="\\"))
    for key,value in [('status',status),('priority',priority),('category_id',category_id),('assigned_user_id',assigned_user_id)]:
        if value is not None: stmt=stmt.where(getattr(Issue,key)==value)
    total=session.scalar(select(func.count()).select_from(stmt.subquery()))
    pages=max(1,(total+per_page-1)//per_page)
    records=session.scalars(stmt.order_by(Issue.updated_at.desc(),Issue.id).offset((page-1)*per_page).limit(per_page)).all()
    return {'records':[issue_dict(x) for x in records],'current_page':page,'total_pages':pages,
            'next_page':page+1 if page<pages else None,'prev_page':page-1 if page>1 else None}


@router.post('',status_code=201)
def create(payload:IssueCreate,session:Session=Depends(get_db)):
    data=payload.model_dump();validate_references(session,data)
    return save_issue(session,Issue(**data))


@router.get('/{issue_id}')
def show(issue_id:str,session:Session=Depends(get_db)):
    return issue_dict(find_issue(session,issue_id))


@router.patch('/{issue_id}')
def update(issue_id:str,payload:IssueUpdate,session:Session=Depends(get_db)):
    issue=find_issue(session,issue_id)
    data=payload.model_dump(exclude_unset=True);validate_references(session,data)
    for key,value in data.items():setattr(issue,key,value)
    return save_issue(session,issue)


@router.delete('/{issue_id}',status_code=204)
def delete(issue_id:str,session:Session=Depends(get_db)):
    session.delete(find_issue(session,issue_id));session.commit()
    return Response(status_code=204)
