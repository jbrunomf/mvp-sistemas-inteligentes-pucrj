from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from api.model.model import Model
from api.model.patient import Patient
from api.model.pipeline import Pipeline
from api.model.preprocessor import PreProcessor
from api.schemas.error_schema import ErrorSchema
from api.schemas.patient_schema import PatientSchema, show_patient, show_all_patients, PatientViewSchema, \
    PatientSearchSchema
from model import *
from logger import logger

from flask_cors import CORS

# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de pacientes com Diabetes")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de pacientes
@app.get('/patient', tags=[paciente_tag],
         responses={"200": PatientSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes cadastrados na base
    Args:
       none

    Returns:
        list: lista de pacientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os pacientes")
    # Criando conexão com a base
    session = Session()
    # Buscando todos os pacientes
    pacientes = session.query(Patient).all()

    if not pacientes:
        # Se não houver pacientes
        return {"pacientes": []}, 200
    else:
        logger.debug(f"%d pacientes econtrados" % len(pacientes))
        print(pacientes)
        return show_all_patients(pacientes), 200


# Rota de adição de paciente
@app.post('/patient', tags=[paciente_tag],
          responses={"200": PatientSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PatientSchema):
    """Adiciona um novo paciente à base de dados
    Retorna uma representação dos pacientes e diagnósticos associados.

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
    model_path = './MachineLearning/pipelines/rf_diabetes_pipeline.pkl'
    # modelo = Model.carrega_modelo(ml_path)
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
        outcome=outcome,
        thal=thal
    )
    logger.debug(f"Adicionando paciente: '{patient}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se paciente já existe na base
        # Adicionando paciente
        session.add(patient)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        # logger.debug(f"Adicionado paciente de nome: '{paciente.name}'")
        return show_patient(patient), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar paciente '{patient}', {error_msg}")
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get('/patient', tags=[paciente_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patient(query: PatientSearchSchema):
    """get pacient by id from database

    Args:
        patient id (int)

    Returns:
        dict: patient instance
    """

    logger.debug(f"loadint patient.. wait a moment #{query.id}")
    session = Session()
    patient = session.query(Patient).filter(Patient.id == query.id).first()

    if not patient:
        error_msg = f"Patient {patient.id} not found. Try again."
        logger.warning(f"{error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Patient found!: '{patient.id}'")
        # retorna a representação do paciente
        return show_patient(patient), 200


# Rota de remoção de paciente por nome
@app.delete('/patient', tags=[paciente_tag],
            responses={"200": PatientViewSchema, "404": ErrorSchema})
def delete_patient(query: PatientSearchSchema):
    """ Delete patient by id
    Args:
        patient id (int)

    Returns:
        msg: success/error message
    """

    patient_id = query.id
    logger.debug(f"Deletando dados sobre paciente #{patient_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando paciente
    patient = session.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{patient_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(patient)
        session.commit()
        logger.debug(f"Deletado paciente #{patient_id}")
        return {"message": f"Paciente {patient_id} removido com sucesso!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
