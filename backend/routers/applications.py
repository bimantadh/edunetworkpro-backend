from api.v1.application.serializers import ApplicationCreate,ApplicationDetails
from fastapi import FastAPI,Depends,HTTPException,status
from db.session import Session, get_session
from api.v1.user.models import User
from api.v1.application.models import Application
from api.v1.consultancy.models import Consultancy
from api.v1.university.models import University,Course
from utils.auth_bearer import jwt_bearer



app = FastAPI()
@app.post("/application")
async def create_application(application: ApplicationCreate, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    try:
        consultancy = db.query(Consultancy).filter(Consultancy.id == application.consultancy_id).first()
        if not consultancy:
            raise HTTPException(status_code=404, detail="Consultancy not found")
        consultancy_id = consultancy.id
        
        university = db.query(University).filter(University.id == application.university_id).first()
        if not university:
            raise HTTPException(status_code=404, detail="University not found")
        university_id= university.id
        
        course = db.query(Course).filter(Course.id == application.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        course_id = course.id
        
        new_application = Application(consultancy_id=consultancy.id, university_id=university.id, course_id=course.id, status=application.status)
        db.add(new_application)
        db.commit()
        db.refresh(new_application)
        return {"message": "Student Application created successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/application/{application_id}", response_model=ApplicationDetails)
def get_application_details(application_id: int, db: Session = Depends(get_session)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    consultancy = db.query(Consultancy).filter(Consultancy.id == application.consultancy_id).first()
    if not consultancy:
        raise HTTPException(status_code=404, detail="Consultancy not found")
    
    university = db.query(University).filter(University.id == application.university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    course = db.query(Course).filter(Course.id == application.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    application_details = ApplicationDetails(
        consultancy_name=consultancy.name,
        university_name=university.name,
        course_name=course.name,
        status=application.status
    )
    return application_details

