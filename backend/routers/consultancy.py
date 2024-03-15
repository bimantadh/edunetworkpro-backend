
@app.get("/consultancy/{consultancy_id}", response_model = ConsultancyDetails)
async def get_consultancy_details(consultancy_id:int, db: Session = Depends(get_session),token: str = Depends(jwt_bearer)):
    consultancy = db.query(Consultancy).filter(Consultancy.id == consultancy_id).first()
    if not consultancy:
        raise HTTPException(status_code=404, detail= "Consultancy not found")
    return consultancy



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
