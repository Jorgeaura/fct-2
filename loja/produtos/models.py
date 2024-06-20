# loja/produtos/models.py
from loja import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(250), nullable=False)
    preco = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(100), nullable=True)
    categoriaId = db.Column(db.Integer, nullable=True)



class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(250), nullable=True)

    def __init__(self, descricao):
        self.descricao = descricao
