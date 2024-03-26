from api.v1.consultancy.models import ConsultancyNotes, Notification
from fastapi import APIRouter,UploadFile,HTTPException
from api.v1.consultancy.serializers import CreateNotes, CreateReminder
from db.session import Session, Depends, get_session,get_current_user



router = APIRouter(prefix="/api/v1")


@router.post("/notes")
async def create_note(note: CreateNotes, db: Session = Depends(get_session)):
    try:
        db_note =ConsultancyNotes(note=note.note, message=note.message)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return {"message": "Note created successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


@router.post("/reminder")
async def create_reminder(note: CreateReminder, db: Session = Depends(get_session)):
    try:
        db_note =ConsultancyNotes(reminder=note.reminder, message=note.message)
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return {"message": "Reminder added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()