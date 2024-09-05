
# from fastapi import APIRouter, Depends, HTTPException

# from ..services import user_account
# from .. import dto
# from ..dependencies import SessionDependency

# router = APIRouter(
#     prefix="/items", #..the prefix must not include a final /.
#     tags=["items"],
#     responses={404: {"description": "Not found"}},
# )

# @router.get("/", response_model=list[dto.Item])
# def read_items(db: SessionDependency, skip: int = 0, limit: int = 100):
#     items = user_account.get_items(db, skip=skip, limit=limit)
#     return items

# @router.post("/", response_model=dto.ItemCreate)
# def create_item(item: dto.ItemCreate):
#     return item
