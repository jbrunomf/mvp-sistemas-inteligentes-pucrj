import sqlalchemy as sa
from datetime import datetime
from typing import Union


from api.model import Base


class Patient(Base):
    __tablename__ = "patients"
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column("Age", sa.Integer, default=0)
    sex = sa.Column("Sex", sa.Integer, default=0)
    cp = sa.Column("ChestPain", sa.Integer, default=0)
    trestbps = sa.Column("RestingBP", sa.Float)
    chol = sa.Column("Cholesterol", sa.Float)
    fbs = sa.Column("FastingBS", sa.Integer, default=0)
    restecg = sa.Column("RestingECG", sa.Integer, default=0)
    thalach = sa.Column("Thalach", sa.Integer, default=0)
    exang = sa.Column("ExerciseAngina", sa.Integer, default=0)
    oldpeak = sa.Column("OldPeak", sa.Float)
    slope = sa.Column("Slope", sa.Integer, default=0)
    ca = sa.Column("Ca", sa.Integer, default=0)
    thal = sa.Column("Thal", sa.Integer, default=0)
    outcome = sa.Column("Outcome", sa.Integer, default=0)
    data_insercao = sa.Column(sa.DateTime, default=datetime.now())

    def __init__(self, age: int, sex: int, cp: int, trestbps: float, chol: float, fbs: int, restecg: int,
                 thalach: int, exang: int, oldpeak: float, slope: int, ca: int, thal: int, outcome: int,
                 date: Union[sa.DateTime, None] = None):
        """
        Create a new patient.
        :param age:
        :param sex:
        :param cp:
        :param trestbps:
        :param chol:
        :param fbs:
        :param restecg:
        :param thalach:
        :param exang:
        :param oldpeak:
        :param slope:
        :param ca:
        :param thal:
        :param outcome:
        :param date:
        """
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal
        self.outcome = outcome
        if date:
            self.date = date
