from api.v1.consultancy.models import ConsultancyNotes, Notification,Inbox, Sent
from fastapi import APIRouter,UploadFile,HTTPException
from api.v1.consultancy.serializers import CreateNotes, CreateReminder, CreateNotification, ShowNotification,InboxMessage, SentMessage,MessageCreate
from db.session import Session, Depends, get_session,get_current_user
from api.v1.user.models import User
from api.v1.consultancy.models import Notification
from typing import List


router = APIRouter(prefix="/api/v1")


@router.post("/notes/{student_id}/note")
async def create_note(student_id: int, note: str, db: Session = Depends(get_session)):
    try:
        user = db.query(User).filter(User.id == student_id, User.type == "student").first()
        if user:
            db_note = ConsultancyNotes.all()
            db.add(db_note)
            db.commit()
            db.refresh(db_note)
            return {"message": "Note created successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        db.close()

@router.post("/reminder/{student_id}")
async def create_reminder(student_id: int, reminder: CreateReminder, db: Session = Depends(get_session)):
    try:
        user = db.query(User).filter(User.id == student_id, User.type == "student").first()
        if user:
            db_note = ConsultancyNotes(student_id=user.id, reminder=reminder.reminder, message=reminder.message)
            db.add(db_note)
            db.commit()
            db.refresh(db_note)
            return {"message": "Reminder added successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student not found")
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


@router.get("/consultancy/all-inboxes", response_model=List[InboxMessage])
async def get_all_inboxes(db: Session = Depends(get_session)):
    inboxes = db.query(Inbox).all()
    return inboxes

@router.get("/consultancy/inbox/{inbox_id}", response_model=List[InboxMessage])
async def get_inbox_by_id(inbox_id: int, db: Session = Depends(get_session)):
    inbox = db.query(Inbox).filter(Inbox.id == inbox_id).first()
    if inbox is None:
        raise HTTPException(status_code=404, detail="Inbox not found")
    return inbox

@router.post("/consultancy/message/send")
async def send_message(message: MessageCreate, db: Session = Depends(get_session)):
    sent_message = Sent(to=message.to, subject=message.subject, message=message.message)
    db.add(sent_message)
    db.commit()
    db.refresh(sent_message)
    return sent_message

@router.get("/consultancy/all-sent", response_model=List[SentMessage])
async def get_all_sent_messages(db: Session = Depends(get_session)):
    sent_messages = db.query(Sent).all()
    return sent_messages