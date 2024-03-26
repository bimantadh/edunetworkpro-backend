from api.v1.user.serializers import UserCreate,TokenSchema,requestdetails, UserDetails
from fastapi import APIRouter,Depends,HTTPException,status
from db.session import Session, get_session, get_current_user
from api.v1.user.models import User
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from api.v1.consultancy.models import Consultancy
from utils.auth_bearer import jwt_bearer



router = APIRouter(prefix="/api/v1/users")

@router.post("/signup")
async def register_user(user: UserCreate, session: Session = Depends(get_session)):
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


@router.get("/me", response_model=UserDetails )
async def users_details(current_user: User = Depends(get_current_user),token: str = Depends(jwt_bearer)):
    user_details = UserDetails(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        type=current_user.type
    )
    return user_details