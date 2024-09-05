from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from typing import List
from typing import Optional
from sqlalchemy import ForeignKey,text
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .database import Base, engine


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     # user relationship
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="items")


class UserType(Base):
    __tablename__ = "user_type"
    user_type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50)) # patient, doctor
    def __repr__(self) -> str:
        return f"user_type(user_type_id={self.user_type_id!r}, name={self.name!r})"

class UserAccount(Base):
    __tablename__ = "user_account"
    user_account_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    birthday:Mapped[Date] = mapped_column(Date)
    patient_doctor_id: Mapped[Optional[int]] = mapped_column(Integer())
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_type.user_type_id"))
    identification_number: Mapped[Optional[str]] = mapped_column(String(100))
    # relation 1 to many
    # email_addresses: Mapped[List["EmailAddress"]] = relationship(
    #     back_populates="user_account", cascade="all, delete-orphan"
    # )
    patient_files: Mapped[List["PatientFile"]] = relationship(
        back_populates="user_account", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"user_account(user_account_id={self.user_account_id!r}, name={self.first_name!r}, fullname={self.last_name!r})"

class FileStatus(Base):
    __tablename__ = "file_status"
    file_status_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    def __repr__(self) -> str:
        return f"file_status(file_status_id={self.file_status_id!r}, name={self.name!r})"


class PatientFile(Base):
    __tablename__ = "patient_file"
    patient_file_id: Mapped[int] = mapped_column(primary_key=True)
    # relation file status
    file_status_id: Mapped[int] = mapped_column(ForeignKey("file_status.file_status_id"))
    file_status: Mapped["FileStatus"] = relationship()
    # relation user account
    user_account_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_account_id"))
    user_account: Mapped["UserAccount"] = relationship(back_populates="patient_files")
    # props
    message: Mapped[Optional[str]] = mapped_column(String(3000))
    path: Mapped[Optional[str]] = mapped_column(String(200))
    prediction_value: Mapped[Optional[int]] = mapped_column(Integer())

# class EmailAddress(Base):
#     __tablename__ = "email_address"
#     address_id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str]
#     user_account_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_account_id"))
#     user_account: Mapped["UserAccount"] = relationship(back_populates="email_addresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.address_id!r}, email_address={self.email_address!r})"


# class ValueLoader:
#     def __init__(self, table : str, prop: str, value :str):
#         self.table = table

#     def get(self):
#         with engine.connect() as conn:
#             query = "SELECT " + self.property_name + " FROM " + self.table  + " WHERE " + self.property_name
#             result = conn.execute(text(query))
#             return result[0]

#  processing_file_status = session.scalars(select(FileStatus).filter_by(name="processing")).first()

class UserTypeValue:
    Doctor = 1
    Patient = 2

class FileStatusValue:
    Enqueue = 1
    Processing = 2
    Success = 3
    Error = 4
