from models import gasto
from state.app_state import AppState

class HomeViewModel:
    def __init__(self):
        self.app_state = AppState()

    @property
    def gastos(self):
        """Retorna a lista de gastos atualizada"""
        return self.app_state.gastos

    @property
    def saldo_total(self) -> float:
        """Calcula o saldo restante subtraindo o total de gastos do salário configurado"""
        salario = self.app_state.config.salario if self.app_state.config else 0.0
        total_gasto = sum(gasto.valor for gasto in self.app_state.gastos)
        return salario - total_gasto

    def handle_excluir(self, id_gasto: int):
        """Delega a exclusão do gasto para o AppState"""
        self.app_state.remover_gasto(id_gasto)
