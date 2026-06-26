from peewee import Proxy, Model

db = Proxy()

class BaseModel(Model):
    """Classe base que os models herdam"""
    class Meta:
        database = db
