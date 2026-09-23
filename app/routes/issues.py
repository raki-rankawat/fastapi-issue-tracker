from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get('/', response_model=list[IssueOut])
def get_issues():
    issues = load_data()
    return issues

@router.post('/', response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(paylod: IssueCreate):
    issues = load_data()
    
    new_issue = {
        "id": str(uuid4()),
        "title": paylod.title,
        "description": paylod.description,
        "priority": paylod.priority,
        "status": IssueStatus.open
    }
    
    issues.append(new_issue)
    save_data(issues)
    return new_issue