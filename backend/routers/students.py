
from api.v1.application.models import Application
from api.v1.consultancy.serializers import StudentDashboard
from fastapi import HTTPException
from db.session import Session, Depends, get_session,get_current_user
from utils.auth_bearer import jwt_bearer
from fastapi import APIRouter
from sqlalchemy import func

router = APIRouter(prefix="/api/v1/student")



@router.get("/dashboard", response_model=StudentDashboard)
def get_student_dashboard(db: Session = Depends(get_session), token: str = Depends(jwt_bearer)):
    try:
        current_user = get_current_user(token, db=db)
        if current_user is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        consultancy_id = current_user.id 

        total_applications = db.query(func.count(Application.id)).scalar()
        in_progress_count = db.query(func.count(Application.id)).filter(Application.status == 'inprogress').scalar()
        accepted_count = db.query(func.count(Application.id)).filter( Application.status == 'accepted').scalar()
        rejected_count = db.query(func.count(Application.id)).filter(Application.status == 'rejected').scalar()
        connected_consultancies = db.query(func.count(Application.consultancy_id)).scalar()
        
        return StudentDashboard(
            applications_submitted=total_applications,
            applications_in_progress=in_progress_count,
            applications_accepted=accepted_count,
            applications_rejected=rejected_count,
            connected_consultancies=connected_consultancies
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")