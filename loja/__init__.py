from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ty4425hk54a21eee5719b9s9df7sdfklx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3242@localhost:3306/shopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Configuração para desativar o tracking de modificações

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Importando rotas após a configuração do SQLAlchemy para evitar ciclos de importação
from loja.admin import rotas as admin_rotas
from loja.produtos import rotas as produtos_rotas

# Aqui você pode adicionar mais imports de outras partes do seu projeto

if __name__ == '__main__':
    app.run(debug=True)
