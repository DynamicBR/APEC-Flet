import datetime
from models.gasto import Gasto
from models.configuracao import Configuracao

def test_configuracao_valores_padrao(db_temporario):
    """Testa se a Configuração assume os valores padrões quando criada vazia"""
    #Cria uma configuração sem passar nenhum parâmetro
    nova_config = Configuracao.create()

    assert nova_config.salario == 0.0
    assert nova_config.frequencia == 1
    assert nova_config.periodo == "Mensal"

def test_configuracao_valores_personalizados(db_temporario):
     """Testa se a Configuração aceita os valores que o usuário informar"""
     nova_config = Configuracao.create(salario=5000.0, frequencia=7, periodo="Semanal")

     assert nova_config.salario == 5000.0
     assert nova_config.frequencia == 7
     assert nova_config.periodo == "Semanal"

def test_gasto_data_padrao(db_temporario):
    """Testa se o Gasto preenche a data automaticamente com o dia de hoje"""
    gasto = Gasto.create(descricao="Internet", categoria="Contas", valor=100.0)

    assert isinstance(gasto.data, datetime.datetime)

    assert gasto.data.year == datetime.datetime.now().year

def test_gasto_formatacao_string(db_temporario):
    """Testa se o metodo __str__ do Gasto formata o texto corretamente para a View"""
    gasto = Gasto.create(descricao="Cinema", categoria="Lazer", valor=35.50)

    texto_formatado = str(gasto)

    assert texto_formatado == "Cinema - R$35.50 (Lazer)"
    assert "Cinema" in texto_formatado
    assert "35.50" in texto_formatado
