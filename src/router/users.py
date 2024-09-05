from fastapi import APIRouter, Depends, HTTPException

from ..services import user_service
from .. import dto
from ..dependencies import SessionDependency

router = APIRouter(
    prefix="/users", #..the prefix must not include a final /.
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=dto.User)
def create_user(user: dto.UserCreate, db: SessionDependency):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)


@router.get("/list", response_model=list[dto.User])
def read_users( db: SessionDependency, skip: int = 0, limit: int = 100):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=dto.User)
def read_user(user_id: int, db: SessionDependency):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @router.post("/{user_id}/items/", response_model=dto.Item)
# def create_item_for_user(
#     user_id: int, item: dto.ItemCreate, db: SessionDependency
# ):
#     return user_account_service.create_user_item(db=db, item=item, user_id=user_id)

