import pytest
from state.app_state import AppState
from models.gasto import Gasto

@pytest.fixture(autouse=True)
def reset_singleton():
    """
    Limpa a instância do Singleton antes e depois de cada teste.
    Garante que um teste não influencie o resultado do outro.
    """
    AppState._instance = None
    yield
    AppState._instance = None

def test_app_state_eh_singleton(db_temporario):
     """Garante que múltiplas chamadas ao AppState retornam a mesma memória"""
     estado1 = AppState()
     estado2 = AppState()

     assert estado1 is estado2

def test_observer_adiciona_e_remove_listener(db_temporario):
    """Testa se as funções de sintonizar estão funcionando"""
    estado = AppState()

    def tela_fake(): pass

    #Testa a adição
    estado.add_listener(tela_fake)
    assert tela_fake in estado._listeners
    assert len(estado._listeners) == 1

    #Testa a remoção
    estado.remove_listener(tela_fake)
    assert tela_fake not in estado._listeners
    assert len(estado._listeners) == 0

def test_observer_notifica_listeners_corretamente(db_temporario):
    """Testa se o estado avisa as telas quando os dados mudam"""
    estado = AppState()

    #Usamos uma lista para registrar se a função foi chamada
    registro_chamadas = []

    def tela_fake_reativa():
        registro_chamadas.append(True)

    estado.add_listener(tela_fake_reativa)

    estado.fetch_dados()

    assert len(registro_chamadas) == 1

def test_adicionar_gasto_atualiza_memoria(db_temporario):
    """Garante que salvar um gasto reflete imediatamente na lista do estado"""
    estado = AppState()

    novo_gasto = Gasto(descricao="Teclado", categoria="Eletrônicos", valor=250.0)

    estado.adicionar_gasto(novo_gasto)

    assert len(estado.gastos) == 1
    assert estado.gastos[0].descricao == "Teclado"
