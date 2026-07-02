import os
from peewee import SqliteDatabase
from pendulum.mixins import default

from models import db
from models.gasto import Gasto
from models.configuracao import Configuracao


class DatabaseManager:
    _instance = None

    def __new__(cls):
        # Implementação Singleton
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._inicializado = False
        return cls._instance

    def __init__(self):
        if not self._inicializado:
            self.init_db()
            self._inicializado = True

    def init_db(self):
        """Configurar banco SQLite, conectando ao Proxy e criando tabelas"""
        # Cria o arquivo gastos.db na raiz do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_dir, 'gasto.db')

        self.sqlite_db = SqliteDatabase(db_path)

        db.initialize(self.sqlite_db)

        self.sqlite_db.connect()
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria as tabelas no banco de dados baseados nos modelos"""
        self.sqlite_db.create_tables([Gasto, Configuracao])

    def listar_gastos(self):
        """Retorna todos os gastos ordenados do mais recente para o mais antigo"""
        # Peewee traduz para: SELECT * FROM gasto ORDDEY BY data DESC;
        return list(Gasto.select().order_by(Gasto.data.desc()))

    def inserir_gasto(self, gasto: Gasto):
        """Salva a instância de um gasto no banco de dados"""
        gasto.save()

    def excluir_gasto(self, id_gasto: int):
        """Exclui um gasto pelo seu ID"""
        Gasto.delete_by_id(id_gasto)

    def obter_configuracao(self):
        """Retorna a configuração do usuário ou cria um padrão se não existir"""
        config, created = Configuracao.get_or_create(id=1,
                                                     defaults={'salario': 0.0, 'frequencia': 1, 'periodo': 'Mensal'})
        return config

    def salvar_configuracao(self, config: Configuracao):
        """Atualiza a configuração salva"""
        config.save()
