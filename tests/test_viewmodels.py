from state.app_state import AppState
from viewmodels.home_viewmodel import HomeViewModel
from viewmodels.estatisticas_viewmodel import EstatisticasViewModel
from models.gasto import Gasto
from models.configuracao import Configuracao


#TESTES HOME VIEWMODEL

def test_home_saldo_total_calculo(db_temporario):
    """Verifica se o saldo total subtrai corretamente os gastos do salário"""
    estado = AppState()

    nova_config = Configuracao.create(salario=3000.0)
    estado.salvar_configuracao(nova_config)

    estado.adicionar_gasto(Gasto(descricao="Mercado", categoria="Alimentação", valor=500.0))
    estado.adicionar_gasto(Gasto(descricao="Luz", categoria="Contas", valor=200.0))

    vm = HomeViewModel()

    assert vm.saldo_total == 2300.0


#TESTE ESTATISTICAS VIEWMODEL

def test_estatisticas_categorias_agrupamento(db_temporario):
    """Verifica se gastos da mesma categoria são somados corretamente"""
    estado = AppState()
    # Adicionando duas "Contas" (100 + 50) e um "Lazer" (30)
    estado.adicionar_gasto(Gasto(descricao="Internet", categoria="Contas", valor=100.0))
    estado.adicionar_gasto(Gasto(descricao="Água", categoria="Contas", valor=50.0))
    estado.adicionar_gasto(Gasto(descricao="Lanche", categoria="Lazer", valor=30.0))

    vm = EstatisticasViewModel()
    categorias = vm.categorias

    assert categorias["Contas"] == 150.0
    assert categorias["Lazer"] == 30.0


def test_estatisticas_maiores_gastos_ordenacao(db_temporario):
    """Verifica se a lógica de Top 5 retorna apenas os 5 maiores e na ordem certa"""
    estado = AppState()

    estado.adicionar_gasto(Gasto(descricao="G1", categoria="A", valor=10.0))
    estado.adicionar_gasto(Gasto(descricao="G2", categoria="A", valor=20.0))
    estado.adicionar_gasto(Gasto(descricao="G3", categoria="A", valor=60.0))
    estado.adicionar_gasto(Gasto(descricao="G4", categoria="A", valor=30.0))
    estado.adicionar_gasto(Gasto(descricao="G5", categoria="A", valor=40.0))
    estado.adicionar_gasto(Gasto(descricao="G6", categoria="A", valor=50.0))

    vm = EstatisticasViewModel()
    top5 = vm.maiores_gastos

    assert len(top5) == 5
    assert top5[0].valor == 60.0