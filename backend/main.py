from api.v1.user.serializers import UserCreate,TokenSchema,requestdetails
from api.v1.university.serializers import UniversityCreate,UniversityDetails, CourseCreate
from api.v1.university.models import University,Course
from api.v1.consultancy.models import Consultancy
from api.v1.application.models import Application
from api.v1.application.serializers import ApplicationCreate, ApplicationDetails
from api.v1.consultancy.serializers import ConsultancyDetails,StudentConsultancy
from typing import Union
import jwt
from datetime import datetime 
from sqlalchemy.orm import joinedload
from api.v1.user.models import User
from db.session import SessionLocal
from db.base_class import Base
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException,status,UploadFile
from fastapi.security import OAuth2PasswordBearer
from utils.auth_bearer import jwt_bearer
from functools import wraps
from utils.utils import create_access_token,create_refresh_token,verify_password,get_hashed_password
from db.session import get_session,get_current_user
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES,REFRESH_TOKEN_EXPIRE_MINUTES,ALGORITHM,JWT_SECRET_KEY,JWT_REFRESH_SECRET_KEY
import mimetypes
from fastapi import FastAPI, UploadFile, File, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
import os, json
from api.v1.file.file import time_str, BASE_DIR, UPLOAD_DIR
import time
from api.v1.file.serializers import UploadedFile
from api.v1.file.models import File


app = FastAPI()


@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=encrypted_password, type=user.type, phone=user.phone)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Check if the user's type is 'consultancy'
    if user.type.lower() == 'consultancy':
        # Create a Consultancy record
        new_consultancy = Consultancy(
            name=f"{user.first_name} {user.last_name}",  # Assuming first_name is used as the name for the consultancy
            email=user.email,
            phone=user.phone,
        )
        session.add(new_consultancy)
        session.commit()

    return {"message": "user created successfully"}

@app.post('/login' ,response_model=TokenSchema)
def login(request: requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    
    db.commit()
   
    return {
        "access_token": access,
        "refresh_token": refresh,
    }
@app.post('/university')
async def create_university(university: UniversityCreate, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    try:
        new_university = University(code=university.code, name=university.name, description=university.description, country=university.country, location=university.location, address=university.address, website=university.website, type=university.type, bachelors_fee=university.bachelors_fee, masters_fee=university.masters_fee, exams=university.exams, established=university.established, icon=university.icon, school_id=university.school_id)
        db.add(new_university)
        db.commit()
        db.refresh(new_university)
        return {"message": "University created successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/university/{university_id}", response_model=UniversityDetails)
async def get_university_details(university_id: int, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    university = db.query(University).filter(University.id == university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    return university

@app.get("/consultancy/{consultancy_id}", response_model = ConsultancyDetails)
async def get_consultancy_details(consultancy_id:int, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    consultancy = db.query(Consultancy).filter(Consultancy.id == consultancy_id).first()
    if not consultancy:
        raise HTTPException(status_code=404, detail= "Consultancy not found")
    return consultancy
    
@app.post("/course")
async def create_course(course: CourseCreate, db:Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    try:
        new_course = Course(code=course.code, name=course.name, description=course.description, level=course.level, fee=course.fee, exams=course.exams, data=course.data, detail_data=course.detail_data)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return {"message": "Course has been created successfully"}
    except Exception as e:
        return {"error": str(e)}



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



@app.get("/consultancy/applications", response_model=list[StudentConsultancy])
def get_consultancy_applications(db: Session = Depends(get_current_user)):
    # applications = db.query(Application).filter(Application.consultancy_id == consultancy_id).all()
    
    # if not applications:
    #     raise HTTPException(status_code=404, detail="No applications found for this consultancy")
    
    consultancy_applications = []
    
    student = db.query(User).filter(User.type == 'student').first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
        
    university = db.query(University).filter(University.id == Application.university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
        
    course = db.query(Course).filter(Course.id == Application.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    student_name = f"{student.first_name} {student.last_name}"
    consultancy_applications.append({
    "student_name": student_name,
    "country_name": university.country,
    "university_applied": university.name,
    "status": Application.status,
    "phone": student.phone
        })
    
    return consultancy_applications


@app.post('/upload/download')
async def upload_download(file: UploadFile, db: Session = Depends(get_session)):
    try:
        content_type, _ = mimetypes.guess_type(file.filename)
        if content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_obj = File(
            
            
            name=file.filename,
            file_type='pdf',  
            mime_type='application/pdf'
        )
        db.add(file_obj)
        db.commit()
        db.refresh(file_obj)

       
        data = await file.read()
        new_filename = f"{os.path.splitext(file.filename)[0]}_{time.time()}.pdf"
        save_path = os.path.join(UPLOAD_DIR, new_filename)

        with open(save_path, "wb") as f:
            f.write(data)

        return FileResponse(path=save_path, media_type="application/octet-stream", filename=new_filename)
    finally:
        db.close()


