from sqlalchemy.orm import Session

from model import User
from schemas import UserSchema


def get_user(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserSchema):
    _user = User(full_name=user.full_name,
                 email=user.email,
                 hashed_password=user.hashed_password,
                 is_active=user.is_active,
                 is_superuser=user.is_superuser)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def delete_user(db: Session, user_id: int):
    _user = get_user_by_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()


def update_user(db: Session,
                user_id: int,
                full_name: str,
                email: str,
                hashed_password: str,
                is_active: bool,
                is_superuser: bool):
    _user = get_user_by_id(db=db, user_id=user_id)
    _user.full_name = full_name
    _user.email = email
    _user.hashed_password = hashed_password
    _user.is_active = is_active
    _user.is_superuser = is_superuser
    db.commit()
    db.refresh(_user)
    return _user
