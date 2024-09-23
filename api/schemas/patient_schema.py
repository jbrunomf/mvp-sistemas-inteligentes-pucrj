from typing import List, Optional

from pydantic import BaseModel

from api.model.patient import Patient


class PatientSchema(BaseModel):
    """ Define como um novo paciente a ser inserido deve ser representado
    """
    age: int = 20
    sex: int = 1
    cp: int = 1
    trestbps: int = 140
    chol: int = 180
    fbs: int = 0
    restecg: int = 2
    thalach: int = 160
    exang: int = 0
    oldpeak: float = 0.1
    thal: int = 3
    slope: int = 1
    ca: int = 0


class PatientViewSchema(BaseModel):
    """Define como um paciente será retornado"""
    age: int = 20
    sex: int = 1
    cp: int = 1
    trestbps: int = 140
    chol: int = 180
    fbs: int = 0
    restecg: int = 2
    thalach: int = 160
    exang: int = 0
    oldpeak: float = 0.
    thal: int = 3
    slope: int = 1
    ca: int = 0
    outcome: None


class PatientSearchSchema(BaseModel):
    """Search patient by id schema"""
    id: int = 0


class ListPacientesSchema(BaseModel):
    """Define a list of patient"""
    patients: List[PatientSchema]


class PacienteDelSchema(BaseModel):
    """ Delete patient Schema """
    id: int = 1


def show_patient(patient: Patient):
    """ Return a patient """
    return {
        "id": patient.id,
        "age": patient.age,
        "sex": patient.sex,
        "cp": patient.cp,
        "trestbps": patient.trestbps,
        "chol": patient.chol,
        "fbs": patient.fbs,
        "restecg": patient.restecg,
        "thalac": patient.thalach,
        "exang": patient.exang,
        "oldpeak": patient.oldpeak,
        "slope": patient.slope,
        "ca": patient.ca,
        "thal": patient.thal,
        "outcome": patient.outcome
    }


# Apresenta uma lista de pacientes
def show_all_patients(patients: List[Patient]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema.
    """
    result = []
    for patient in patients:
        result.append({
            "id": patient.id,
            "age": patient.age,
            "sex": patient.sex,
            "cp": patient.cp,
            "trestbps": patient.trestbps,
            "chol": patient.chol,
            "fbs": patient.fbs,
            "restecg": patient.restecg,
            "thalac": patient.thalach,
            "exang": patient.exang,
            "oldpeak": patient.oldpeak,
            "slope": patient.slope,
            "ca": patient.ca,
            "thal": patient.thal,
            "outcome": patient.outcome
        })

    return result
