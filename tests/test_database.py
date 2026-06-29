from database.database_manager import DatabaseManager
from models.gasto import Gasto

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
