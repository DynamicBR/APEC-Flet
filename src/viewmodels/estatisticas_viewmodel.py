from collections import defaultdict
from models.configuracao import Configuracao
from models.gasto import Gasto
from state.app_state import AppState
import datetime


class EstatisticasViewModel:
    def __init__(self):
        self.app_state = AppState()
        # Inicializa a lista filtrada contendo todos os gastos por padrão
        self.gastos_filtrados = self.app_state.gastos

    @property
    def total(self) -> float:
        """Retorna a soma de todos os gastos do período filtrado"""
        return sum(gasto.valor for gasto in self.gastos_filtrados)

    @property
    def categories(self) -> dict:  # Mantido propriedade compatível com a chamada
        return self.categorias

    @property
    def categorias(self) -> dict:
        """Agrupa os gastos filtrados por categoria e soma os valores"""
        resumo = defaultdict(float)
        for gasto in self.gastos_filtrados:
            resumo[gasto.categoria] += gasto.valor
        return dict(resumo)

    @property
    def maiores_gastos(self):
        """Retorna o "Top 5" dos maiores gastos do período filtrado"""
        gastos_ordenados = sorted(self.gastos_filtrados, key=lambda g: g.valor, reverse=True)
        return gastos_ordenados[:5]

    def carregar_dados(self, filtro_strategy="Todos", data_inicio=None, data_fim=None):
        """
        Aplica as regras de filtragem na lista em memória.
        """
        hoje = datetime.date.today()
        all_gastos = self.app_state.gastos

        # Helper para garantir que comparamos objetos date puros (segurança contra Datetime)
        def extrair_data(d):
            if isinstance(d, datetime.datetime):
                return d.date()
            return d

        if filtro_strategy == "Este Mês":
            self.gastos_filtrados = [
                g for g in all_gastos
                if extrair_data(g.data).month == hoje.month and extrair_data(g.data).year == hoje.year
            ]
        elif filtro_strategy == "Esta Semana":
            sete_dias_atras = hoje - datetime.timedelta(days=7)
            self.gastos_filtrados = [
                g for g in all_gastos
                if extrair_data(g.data) >= sete_dias_atras
            ]
        else:
            self.gastos_filtrados = all_gastos