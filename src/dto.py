from pydantic import BaseModel
from datetime import datetime, date, time

## item

# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
#         from_attributes = True

## user

# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     # items: list[Item] = []

#     class Config:
#         from_attributes = True


class UserSessionModel:
    user_id:int
    email:str



class PatientDto(BaseModel):
    user_account_id: int
    email:str
    first_name : str
    last_name: str
    patient_doctor_id: int
    user_type_id: int
    identification_number:str
    birthday: date

    class Config:
        from_attributes = True


class PatientUpsertResponseDto(BaseModel):
    user_account_id: int
    first_name : str
    last_name: str
    patient_doctor_id: int
    user_type_id: int
    identification_number:str

    class Config:
        from_attributes = True



class PatientCreate(BaseModel):
    patient_doctor_id:int
    first_name:str
    last_name:str
    email:str
    identification_number:str
    birthday:date #In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.

class PatientUpdate(BaseModel):
    user_account_id:int #pk
    first_name:str
    last_name:str
    email:str
    identification_number:str
    birthday:date #In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.
