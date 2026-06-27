from collections import defaultdict
from models.configuracao import Configuracao
from models.gasto import Gasto
from state.app_state import AppState

class EstatisticasViewModel:
    def __init__(self):
        self.app_state = AppState()

    @property
    def total(self) -> float:
        """Retorna a soma de todos os gastos registrados"""
        return sum(gasto.valor for gasto in self.app_state.gastos)

    @property
    def categorias(self) -> dict:
        """Agrupa os gastos por categoria e soma os valores"""
        resumo = defaultdict(float)
        for gasto in self.app_state.gastos:
            resumo[gasto.categoria] += gasto.valor

        return dict(resumo)

    @property
    def maiores_gastos(self):
        """Retorna o "Top 5" dos maiores gastos do usuário"""
        gastos_ordenados = sorted(self.app_state.gastos, key=lambda g: g.valor, reverse=True)
        return gastos_ordenados[:5]

    def carregar_dados(self, filtro_strategy=None, data_inicio=None, data_fim=None):
        pass
