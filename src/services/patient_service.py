
from sqlalchemy.orm import Session
from sqlalchemy import select

from src import dto
from typing import List
from src.models import UserAccount, UserTypeValue
from fastapi import FastAPI, HTTPException

def find_by_id(db:Session, patient_id: int):
    patient = db.scalars(select(UserAccount).filter_by(user_account_id=patient_id)).first()
    return patient

def find_by_email(db:Session, email: str):
    patient = db.scalars(select(UserAccount).filter_by(email=email)).first()
    return patient

def get_patients_by_doctor_id(db:Session, doctor_id:int, skip: int = 0, limit: int = 100 ) -> List[UserAccount]:
    result = db.query(UserAccount).filter_by(patient_doctor_id=doctor_id).offset(skip).limit(limit).all()
    return result

def create_patient(db:Session,  patient_dto: dto.PatientCreate):
    db_user = find_by_email(db, email=patient_dto.email)
    if db_user:
        print(db_user.user_account_id)
        print(db_user.email + ' -- dto:'+patient_dto.email)
        raise HTTPException(status_code=400, detail="Email already registered")
    patient = UserAccount()
    patient.first_name = patient_dto.first_name
    patient.last_name = patient_dto.last_name
    patient.patient_doctor_id = patient_dto.patient_doctor_id
    patient.identification_number = patient_dto.identification_number
    patient.birthday = patient_dto.birthday
    patient.email = patient_dto.email
    patient.user_type_id = UserTypeValue.Patient
    db.add(patient)
    db.commit()
    return patient

def update_patient(db:Session, patient_id:int, patient_dto: dto.PatientUpdate):
    result = db.query(UserAccount).filter_by(user_account_id=patient_id).first()
    if not result:
         raise HTTPException(status_code=404, detail="Record not found")
    db.query(UserAccount) \
        .filter_by(user_account_id=patient_dto.user_account_id) \
        .update({
            'first_name': patient_dto.first_name,
            'last_name': patient_dto.last_name,
            'identification_number': patient_dto.identification_number,
            'email': patient_dto.email,
            'birthday': patient_dto.birthday,
        })
    db.commit()