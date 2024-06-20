from flask_login import UserMixin
from loja import db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)

class Utilizador(UserMixin, db.Model):
    __tablename__ = 'utilizadores'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)  

    roleId = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref=db.backref('utilizadores', lazy=True))
    
    

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')


    def check_password(self, password):
        
        return self.password == password
    
    def __repr__(self):
        return '<Utilizador %r>' % self.email

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    morada = db.Column(db.String(100), nullable=True)
    utilizadorId = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    utilizador = db.relationship('Utilizador', backref=db.backref('cliente', uselist=False))

    def __repr__(self):
        return f'<Cliente {self.nome}>'

class LinhaEncomenda(db.Model):
    __tablename__ = 'linhas_encomenda'
    id = db.Column(db.Integer, primary_key=True)
    encomendaId = db.Column(db.Integer, db.ForeignKey('encomendas.id'), nullable=False)
    produtoId = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

class Encomenda(db.Model):
    __tablename__ = 'encomendas'
    id = db.Column(db.Integer, primary_key=True)
    clienteId = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    dataEncomenda = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
