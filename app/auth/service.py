from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password
from app.users.models import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter_by(email=email).one_or_none()
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_user(db: Session, email: str, password: str) -> User:
    existing = db.query(User).filter_by(email=email).one_or_none()
    if existing is not None:
        raise ValueError("Email already registered")

    user = User(email=email, password=hash_password(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered") from None
    db.refresh(user)
    return user
