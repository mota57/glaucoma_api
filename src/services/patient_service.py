
from sqlalchemy.orm import Session
from sqlalchemy import select

from src import dto
from typing import List
from src.models import FileStatusValue, PatientFile, UserAccount, UserTypeValue
from fastapi import HTTPException

from PIL import Image
import base64
import uuid
import joblib
import boto3
import numpy as np
import io

s3 = boto3.client("s3")

def find_by_id(db:Session, patient_id: int):
    patient = db.scalars(select(UserAccount).filter_by(user_account_id=patient_id)).first()
    return patient

def find_by_email(db:Session, email: str):
    patient = db.scalars(select(UserAccount).filter_by(email=email)).first()
    return patient

def get_patients_by_doctor_id(db:Session, doctor_id:int, skip: int = 0, limit: int = 100 ) -> List[UserAccount]:
    result = db.query(UserAccount).filter_by(patient_doctor_id=doctor_id).offset(skip).limit(limit).all()
    return result

def list_patient_files(db:Session, patient_id: int):
    patient_files = db.query(PatientFile).filter(PatientFile.user_account_id == patient_id).all()
    return patient_files or []

def create_patient_file(db:Session, patient_file: dto.PatientFileCreate):
    user_account = db.query(UserAccount).filter(UserAccount.user_account_id == patient_file.user_account_id).first()
    if not user_account:
        raise HTTPException(status_code=404, detail="User account not found")

    result = process_image_prediction(file=patient_file.file,file_name_param=patient_file.fileName)

    new_patient_file = PatientFile(
        user_account_id=patient_file.user_account_id,
        file_status_id=FileStatusValue.Success,
        message=result.message,
        path=result.path,
        prediction_value=int(result.prediction)
    )

    db.add(new_patient_file)
    db.commit()
    result.patient_file_id = new_patient_file.patient_file_id
    return result

def process_image_prediction(file:str, file_name_param:str):
    """
    - get the prediction of the file from json_data.get('file').
    - save the file on s3.
    - append the filename, the prediction to the files of the patient.
    """
    # Decode base64 file content
    file_content = base64.b64decode(file)
    file_name = __generate_file_name(file_name_param)
    print('file_name ==> ' + file_name)
    # Upload the file to S3
    s3.put_object(
        Bucket='glaucoma-website-107594336623',
        Key="images/" + file_name,
        Body=file_content,
    )
    # call prediction
    prediction = __get_prediction_with_knn(file_content)
    # return dto
    result = dto.FileProcessDTO()
    result.success= True
    result.message= "Processed image file name " + file_name
    result.prediction= str(prediction)
    result.file_name= file_name
    result.path= "/images/" + file_name
    return result

def __generate_file_name(filename:str):
    # Generate a unique filename for the S3 object
    file_extension = filename.split(".")[1]
    file_name = str(uuid.uuid4()).replace('-', '') + '.' + file_extension
    return file_name

def __get_prediction_with_knn(file_content: str | bytes):
    # from image to image array
    img_array = __from_image_to_array(file_content)
    # load the model
    loaded_model = joblib.load('./src/data/knn_model.joblib')
    # Make predictions on new data
    prediction = loaded_model.predict([img_array])[0]
    return prediction


def __from_image_to_array(file_content):
    img = Image.open(io.BytesIO(file_content)).convert('L')  # Convert to grayscale
    img = img.resize((64, 64))  # Resize to 64x64 pixels
    img_array = np.array(img).flatten()  # Flatten the image to a 1D array
    return img_array

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