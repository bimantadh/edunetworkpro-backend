from api.v1.consultancy.models import ConsultancyNotes, Notification
from fastapi import APIRouter,UploadFile,HTTPException
from api.v1.consultancy.serializers import CreateNotes, CreateReminder, CreateNotification, ShowNotification
from db.session import Session, Depends, get_session,get_current_user
from api.v1.user.models import User
from api.v1.consultancy.models import Notification
from typing import List


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



@router.post("/notifications")
async def create_notification(notification: CreateNotification,db: Session = Depends(get_session)):
    try:
        db_notification =Notification(message=notification.message, notification_from = notification.notification_from, student_name = notification.student_name, type = notification.type)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return {"message": "Notification added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()


@router.get("/notification/{note_id}", response_model=ShowNotification)
async def get_notification(note_id: int, db: Session = Depends(get_session)):
    db_notify = db.query(Notification).filter(Notification.id == note_id).first()
    if db_notify is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return ShowNotification(
        message=db_notify.message,
        notification_from=db_notify.notification_from,
        student_name=db_notify.student_name,
        type=db_notify.type
    )


@router.get("/notification", response_model=List[ShowNotification])
async def get_notification(db: Session = Depends(get_session)):
    db_notifications = db.query(Notification).all()
    return [
        ShowNotification(
            message=db_notify.message,
            notification_from=db_notify.notification_from,
            student_name=db_notify.student_name,
            type=db_notify.type
        ) for db_notify in db_notifications
    ]