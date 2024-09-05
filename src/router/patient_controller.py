
from fastapi import APIRouter, Depends, HTTPException

from src.services import patient_service
from src import dto
from src.dependencies import SessionDependency

router = APIRouter(
    prefix="/patient", #..the prefix must not include a final /.
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list/{doctor_id}")
def list(db: SessionDependency, doctor_id:int= 0, skip: int = 0, limit: int = 100):
    result = patient_service.get_patients_by_doctor_id(db=db, doctor_id=doctor_id, skip=skip, limit=limit)
    return result


@router.post("/create", response_model=dto.PatientUpsertResponseDto)
def create(db: SessionDependency, patient_dto: dto.PatientCreate):
    return patient_service.create_patient(db=db, patient_dto=patient_dto)

@router.put("/update/{patient_id}", response_model=dto.PatientUpsertResponseDto)
def update(patient_id:int, db: SessionDependency, patient_dto: dto.PatientUpdate):
    return patient_service.update_patient(db=db, patient_dto=patient_dto)