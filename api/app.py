import pickle
import pandas as pd
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from api.model.model import Model
from api.model.patient import Patient
from api.model.pipeline import Pipeline
from api.model.preprocessor import PreProcessor
from api.schemas.error_schema import ErrorSchema
from api.schemas.patient_schema import PatientSchema, show_patient, show_all_patients, PatientViewSchema, \
    PatientSearchSchema, ListPacientesSchema
from api.model import *
from api.logger import logger
from flask_cors import CORS

from api.tests.model_test import ModelAccuracyAssertion
import warnings
warnings.filterwarnings("ignore")

info = Info(title="Heart Disease Prediction", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Doc", description="Swagger, Redoc or RapiDoc")
patient_tag = Tag(name="Patient", description="Create, Read Data from patients")


@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, a screen that allows choosing the style of documentation.
    """
    return redirect('/openapi')


@app.get('/patient', tags=[patient_tag],
         responses={"200": ListPacientesSchema, "404": ErrorSchema})
def get_all():
    """Lists all patients registered in the database
    Args:
       none

    Returns:
        list: list of patients registered in the database
    """
    logger.debug("Collecting data on all patients")
    # Creating connection to the database
    session = Session()
    # Fetching all patients
    patients = session.query(Patient).all()

    if not patients:
        # If there are no patients
        return {"patients": []}, 200
    else:
        logger.debug(f"%d patient(s) found" % len(patients))
        return show_all_patients(patients), 200


@app.get('/patient/id', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patient(query: PatientSearchSchema):
    """get patient by id from database

    Args:
        patient id (int)

    Returns:
        dict: patient instance
    """

    logger.debug(f"loading patient.. wait a moment #{query.id}")
    session = Session()
    patient = session.query(Patient).filter(Patient.id == query.id).first()

    if not patient:
        error_msg = f"Patient {patient.id} not found. Try again."
        logger.warning(f"{error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Patient found!: '{patient.id}'")
        return show_patient(patient), 200


@app.post('/patient', tags=[patient_tag],
          responses={"200": PatientSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PatientSchema):
    """
    Predicts and adds a new patient to the database.
    
    This function:
    1. Loads a pre-trained machine learning model from a serialized pickle file.
    2. Validates the model's accuracy with existing test data.
    3. Extracts necessary patient information from the given form.
    4. Prepares the patient data for model input.
    5. Uses the model to predict the outcome for the new patient.
    6. Adds the new patient and their diagnosis to the database.
    
    Args:
        form (PatientSchema): Form containing patient information.

    Returns:
        tuple: A tuple containing a dictionary representation of the patient and the HTTP status code.
    """
    with open('MachineLearning/pipelines/pipeline.pkl', 'rb') as file:
        classifer = pickle.load(file)
    X_test_file = pd.read_csv('api/tests/x_test_heart_disease.csv')
    y_test_file = pd.read_csv('api/tests/y_test_heart_disease.csv')

    assertion = ModelAccuracyAssertion(classifer, X_test_file, y_test_file, threshold=0.7)
    assertion.assert_accuracy()

    """Adds a new patient to the database
    Returns a representation of patients and associated diagnoses.

    Args:
        age: Age of the patient (in years)
        sex: Sex of the patient (1 = male, 0 = female)
        cp: Chest pain type (1-4)
        trestbps: Resting blood pressure (in mm Hg on admission to the hospital)
        chol: Serum cholesterol in mg/dl
        fbs: Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
        restecg: Resting electrocardiographic results (0-2)
        thalach: Maximum heart rate achieved
        exang: Exercise-induced angina (1 = yes; 0 = no)
        oldpeak: ST depression induced by exercise relative to rest
        slope: Patient's Slope Levels++]
        ca: Patient's CA Levels
        thal: Patient's THAL Levels
        outcome: target to predict

    Returns:
        dict: patient
        :param form:
    """

    # Recuperando os dados do formulário
    age = form.age
    sex = form.sex
    cp = form.cp
    trestbps = form.trestbps
    chol = form.chol
    fbs = form.fbs
    restecg = form.restecg
    thalach = form.thalach
    exang = form.exang
    oldpeak = form.oldpeak
    slope = form.slope
    ca = form.ca
    thal = form.thal

    # Preparando os dados para o modelo
    X_input = PreProcessor.prepare_from_form(form)
    # Carregando modelo
    model_path = 'MachineLearning/pipelines/pipeline.pkl'
    # modelo = Model.load_model(model_path)
    modelo = Pipeline.load(model_path)
    # Realizando a predição
    outcome = int(Model.predict(modelo, X_input)[0])
    patient = Patient(
        age=age,
        sex=sex,
        cp=cp,
        trestbps=trestbps,
        chol=chol,
        fbs=fbs,
        restecg=restecg,
        thalach=thalach,
        exang=exang,
        oldpeak=oldpeak,
        slope=slope,
        ca=ca,
        thal=thal,
        outcome=outcome
    )

    #logger.debug(f"Adding patient: '{patient}'")

    try:
        # Creating connection to the database
        session = Session()

        # Checking if patient already exists in the database
        # Adding patient
        session.add(patient)
        # Committing the addition command
        session.commit()
        # Concluding the transaction
        # logger.debug(f"Added patient with name: '{paciente.name}'")
        return show_patient(patient), 200

    except Exception as e:
        error_msg = "Could not save the patient"
        logger.warning(f"Error adding patient '{patient}', {e}")
        return {"message": error_msg}, 400


@app.delete('/patient', tags=[patient_tag],
            responses={"200": PatientViewSchema, "404": ErrorSchema})
def delete_patient(query: PatientSearchSchema):
    """ Delete patient by id
    Args:
        patient id (int)

    Returns:
        msg: success/error message
    """

    patient_id = query.id
    logger.debug(f"Deleting data on patient #{patient_id}")

    # Creating connection to the database
    session = Session()

    # Fetching patient
    patient = session.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        error_msg = "Patient not found in the database :/"
        logger.warning(f"Error deleting patient '{patient_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(patient)
        session.commit()
        logger.debug(f"Deleted patient #{patient_id}")
        return {"message": f"Patient {patient_id} successfully removed!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
