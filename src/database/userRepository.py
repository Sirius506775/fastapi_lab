from typing import List

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.orm import User
from database.connection import get_db


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_by_username(self, username: str) -> User | None:
        return self.session.scalars(select(User).where(User.username == username)).first()

    def save_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()  # db save
        self.session.refresh(instance=user)
        return user
