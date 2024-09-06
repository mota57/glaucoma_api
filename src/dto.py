from pydantic import BaseModel
from datetime import date, datetime

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

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class requestdetails(BaseModel):
    email:str
    password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime

# class User(UserBase):
#     id: int
#     is_active: bool
#     # items: list[Item] = []

#     class Config:
#         from_attributes = True


class UserSessionModel:
    user_id: int
    email: str


class PatientDto(BaseModel):
    user_account_id: int
    email: str
    first_name: str
    last_name: str
    patient_doctor_id: int
    user_type_id: int
    identification_number: str
    birthday: date

    class Config:
        from_attributes = True


class PatientUpsertResponseDto(BaseModel):
    user_account_id: int
    first_name: str
    last_name: str
    patient_doctor_id: int
    user_type_id: int
    identification_number: str

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    patient_doctor_id: int
    first_name: str
    last_name: str
    email: str
    identification_number: str
    birthday: date  # In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.


class PatientUpdate(BaseModel):
    user_account_id: int  # pk
    first_name: str
    last_name: str
    email: str
    identification_number: str
    birthday: date  # In requests and responses will be represented as a str in ISO 8601 format, like: 2008-09-15.


# Pydantic models
class PatientFileCreate(BaseModel):
    user_account_id:int
    fileName:str
    file: str

class PatientFileViewDto(BaseModel):
    patient_file_id:int
    file_status_id:int
    user_account_id:int
    message:str
    path:str
    prediction_value:int

    class Config:
        from_attributes = True


class FileProcessDTO:
    file_status_id:int
    success: bool
    message: str
    prediction: str
    file_name: str
    path: str
