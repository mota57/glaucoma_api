from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

from src.auth_bearer import JWTBearer
from src.services import patient_service
from src import dto
from src.dependencies import SessionDependency
from typing import List

router = APIRouter(
    prefix="/patient",  # ..the prefix must not include a final /.
    tags=["patients"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer())]
)




@router.get("/list/{doctor_id}",response_model=List[dto.PatientDto])
def list(db: SessionDependency, req: Request, skip: int = 0, limit: int = 100):
    result = patient_service.get_patients_by_doctor_id(
        db=db, doctor_id=req.state.user_id, skip=skip, limit=limit
    )
    return result


@router.post("/create", response_model=dto.PatientUpsertResponseDto)
def create(db: SessionDependency, req:Request, patient_dto: dto.PatientCreate):
    patient_dto.patient_doctor_id = req.state.user_id
    return patient_service.create_patient(db=db, patient_dto=patient_dto)


@router.put("/update/{patient_id}")
def update(patient_id: int, db: SessionDependency, patient_dto: dto.PatientUpdate):
    # todo validate only doctor from request.state.user-id can change it.
    patient_service.update_patient(
        db=db, patient_id=patient_id, patient_dto=patient_dto
    )
    return {"success": True}


@router.get("/list_patient_files", response_model=List[dto.PatientFileViewDto])
def list_patient_files(db: SessionDependency, patient_id:int = 0):
    result = patient_service.list_patient_files(db=db, patient_id=patient_id)
    return result

@router.post("/create_patient_file")
def create_patient_file(db: SessionDependency, data: dto.PatientFileCreate):
    result = patient_service.create_patient_file(db=db, patient_file=data)
    return result

