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
