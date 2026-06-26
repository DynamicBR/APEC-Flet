from peewee import FloatField, IntegerField, CharField
from . import BaseModel

class Configuracao(BaseModel):
    salario = FloatField(default=0.0)
    frequencia = IntegerField(default=1)
    periodo = CharField(default="Mensal")
