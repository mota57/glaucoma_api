
from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine, Base
from src.models import FileStatus, UserType

router = APIRouter(
    prefix="/database",
    tags=["database"],
    responses={404: {"description": "Not found"}}
)

@router.post("/seed_db")
def seed_db(db:Session):
    # pylint: disable-next=not-callable
    total_status = select(func.count('*')).select_from(FileStatus)
    if total_status == 0:
        db.add_all([
            FileStatus(name="enqueue"),
            FileStatus(name="processing"),
            FileStatus(name="success"),
            FileStatus(name="error")
        ])
        print('adding FileStatus')
        db.commit()
    # adding user type
    # pylint: disable-next=not-callable
    total_user_types = select(func.count('*')).select_from(UserType)
    if total_user_types == 0:
        db.add_all([
            UserType(name="doctor"),
            UserType(name="patient"),
        ])
        print('adding user_types')
        db.commit()