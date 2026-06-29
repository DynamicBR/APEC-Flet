import pytest
import sys
import os
from peewee import SqliteDatabase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from state.app_state import AppState
from models import db
from models.configuracao import Configuracao
from models.gasto import Gasto

@pytest.fixture
def db_temporario():
    """Cria um banco de dados temporário na RAM para os testes"""
    #Cria o banco em memória
    test_db = SqliteDatabase(':memory:')

    #Conecta o Proxy a este banco temporário
    db.initialize(test_db)
    test_db.connect()
    test_db.create_tables([Gasto, Configuracao])

    #Entrega o ambiente limpo para o teste rodar
    yield

    test_db.drop_tables([Gasto, Configuracao])
    test_db.close()

@pytest.fixture(autouse=True)
def reset_singleton():
    """
    Limpa a instância do Singleton antes e depois de cada teste.
    Garante que um teste não influencie o resultado do outro.
    """
    AppState._instance = None
    yield
    AppState._instance = None
