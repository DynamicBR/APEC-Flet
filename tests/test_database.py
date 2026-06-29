import pytest
import sys
import os
from peewee import SqliteDatabase

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from database.database_manager import DatabaseManager
from models import db
from models.gasto import Gasto
from models.configuracao import Configuracao

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

# TESTES REAIS

def test_inserir_e_listar_gastos(db_temporario):
    """Testa se o DatabaseManager consegue salvar e ler um gasto"""
    #Preparação
    manager = DatabaseManager()
    manager._inicializado = True

    novo_gasto = Gasto(descricao="Pizza", categoria="Alimentação", valor=50.0)

    #Ação
    manager.inserir_gasto(novo_gasto)
    lista_gastos = manager.listar_gastos()

    #Verificação
    assert len(lista_gastos) == 1
    assert lista_gastos[0].descricao == "Pizza"
    assert lista_gastos[0].valor == 50.0
