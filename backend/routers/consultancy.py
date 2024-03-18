from api.v1.consultancy.models import Consultancy
from api.v1.university.models import University,Course
from api.v1.user.models import User
from api.v1.application.models import Application
from api.v1.consultancy.serializers import ConsultancyDetails,StudentConsultancy
from fastapi import HTTPException
from db.session import Session, Depends, get_session,get_current_user
from utils.auth_bearer import jwt_bearer
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/consultancy/{consultancy_id}", response_model = ConsultancyDetails)
async def get_consultancy_details(consultancy_id:int, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    consultancy = db.query(Consultancy).filter(Consultancy.id == consultancy_id).first()
    if not consultancy:
        raise HTTPException(status_code=404, detail= "Consultancy not found")
    return consultancy




@router.get("/consultancy/applications", response_model=list[StudentConsultancy])
def get_consultancy_applications(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    consultancy_id = current_user.id 
    
    applications = db.query(Application).filter(Application.consultancy_id == consultancy_id).all()
    
    if not applications:
        raise HTTPException(status_code=404, detail="No applications found for this consultancy")
    
    consultancy_applications = []
    
    for application in applications:
        student = db.query(User).filter(User.id == application.user_id).first()  # Fetching user who created the application
        
        university = db.query(University).filter(University.id == application.university_id).first()
        if not university:
            raise HTTPException(status_code=404, detail="University not found")
        
        course = db.query(Course).filter(Course.id == application.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        student_name = f"{student.first_name} {student.last_name}"
        consultancy_applications.append({
            "student_name": student_name,
            "country_name": university.country,
            "university_applied": university.name,
            "course_name": course.name,
            "status": application.status,
            "phone": student.phone
        })
    
    return consultancy_applications