from database.database_manager import DatabaseManager
from models.gasto import Gasto
from models.configuracao import Configuracao

class AppState:
    _instance = None

    def __new__(cls):
        # O AppState também é um Singleton mas com um Observer
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if not self._inicializado:
            self.db_manager = DatabaseManager()

            self.gastos: list[Gasto] = []
            self.config: Configuracao = None

            self._listeners = []
            self._inicializado = True

    def add_listener(self, listener_callback):
        """Sintoniza uma tela para ouvir as atualizações de estado"""
        if listener_callback not in self._listeners:
            self._listeners.append(listener_callback)

    def remove_listener(self, listener_callback):
        """Remove a tela dos ouvintes"""
        # Correção: Agora verifica se está na lista antes de remover
        if listener_callback in self._listeners:
            self._listeners.remove(listener_callback)

    def notificar_listeners(self):
        """Avisa todas as telas sintonizadas que elas precisam se atualizar"""
        for listener in self._listeners:
            listener()

    def fetch_dados(self):
        """Busca os dados mais recentes do banco e atualiza a memória"""
        self.gastos = self.db_manager.listar_gastos()
        self.config = self.db_manager.obter_configuracao()
        self.notificar_listeners()

    def adicionar_gasto(self, gasto: Gasto):
        """Salva no banco, busca a lista atualizada e avisa as telas"""
        self.db_manager.inserir_gasto(gasto)
        self.fetch_dados()

    def remover_gasto(self, id_gasto: int):
        """Remove do banco, busca a lista atualizada e avisa as telas"""
        self.db_manager.excluir_gasto(id_gasto)
        self.fetch_dados()

    def salvar_configuracao(self, nova_config: Configuracao):
        """Atualiza as configurações no banco e avisa as telas"""
        self.db_manager.salvar_configuracao(nova_config)
        self.fetch_dados()