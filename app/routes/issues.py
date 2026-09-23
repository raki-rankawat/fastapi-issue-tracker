from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get('/', response_model=list[IssueOut])
def get_issues():
    issues = load_data()
    return issues

@router.get('/{issue_id}', response_model=IssueOut)
def get_issue(issue_id: str):
    issues = load_data()
    for issue in issues:
        if issue['id'] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Issue not found')

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

@router.put('/{issue_id}', response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:
            updated_issue = issue.copy()

            if payload.title is not None:
                updated_issue["title"] = payload.title

            if payload.description is not None:
                updated_issue["description"] = payload.description

            if payload.priority is not None:
                updated_issue["priority"] = payload.priority

            if payload.status is not None:
                updated_issue["status"] = payload.status

            issues[index] = updated_issue
            save_data(issues)
            return updated_issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")

@router.delete('/{issue_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str):
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue["id"] == issue_id:
            issues.pop(index)
            save_data(issues)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")