from api.v1.university.models import University,Course
from api.v1.university.serializers import UniversityCreate, UniversityDetails, CourseCreate
from fastapi import HTTPException, APIRouter
from utils.auth_bearer import jwt_bearer

from db.session import Session, Depends, get_session,get_current_user


router = APIRouter(prefix="/api/v1")


@router.post('/university')
async def create_university(university: UniversityCreate, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    try:
        new_university = University(code=university.code, name=university.name, description=university.description, country=university.country, location=university.location, address=university.address, website=university.website, type=university.type, bachelors_fee=university.bachelors_fee, masters_fee=university.masters_fee, exams=university.exams, established=university.established, icon=university.icon, school_id=university.school_id)
        db.add(new_university)
        db.commit()
        db.refresh(new_university)
        return {"message": "University created successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/university/{university_id}", response_model=UniversityDetails)
async def get_university_details(university_id: int, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    return university


   
@router.post("/course")
async def create_course(course: CourseCreate, db:Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    try:
        new_course = Course(code=course.code, name=course.name, description=course.description, level=course.level, fee=course.fee, exams=course.exams, data=course.data, detail_data=course.detail_data)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return {"message": "Course has been created successfully"}
    except Exception as e:
        return {"error": str(e)}
