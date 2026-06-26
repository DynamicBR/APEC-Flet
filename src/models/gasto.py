import datetime
from peewee import CharField, FloatField, DateField
from . import BaseModel

class Gasto(BaseModel):
    descricao = CharField()
    categoria = CharField()
    valor = FloatField()
    data = DateField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.descricao} - R${self.valor:.2f} ({self.categoria})"
