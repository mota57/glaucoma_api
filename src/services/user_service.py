# from sqlalchemy.orm import Session

# from .. import models, dto


# def get_user(db: Session, user_id: int):
#     return db.query(models.UserAccount).filter(models.UserAccount.user_account_id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.UserAccount).filter(models.UserAccount.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.UserAccount).offset(skip).limit(limit).all()


# def create_user(db: Session, user: dto.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.UserAccount(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: dto.ItemCreate, user_id: int):
#     db_item = models.Item(**item.model_dump(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item