from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.dto import UserSessionModel
from fastapi.security import OAuth2PasswordBearer

# from fastapi import Header, HTTPException

# async def get_token_header(x_token: Annotated[str, Header()]):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


# async def get_query_token(token: str):
#     if token != "jessica":
#         raise HTTPException(status_code=400, detail="No Jessica token provided")

def get_db():
    """
    https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
    FastAPI supports dependencies that do some extra steps after finishing.  <br/>
    To do this, use yield instead of return, and write the extra steps (code) after.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
async def get_current_user():
    user = fake_decode_token(token)
    return user

SessionDependency = Annotated[Session, Depends(get_db)]
UserSessionModelDep = Annotated[UserSessionModel, Depends(get_db)]
