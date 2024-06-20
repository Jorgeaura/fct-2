# loja/admin/rotas.py
from flask import render_template, session, request, redirect, url_for, flash
from loja import app, db
from loja.admin.forms import LoginForm, RegisterForm
from loja.admin.models import Role, Utilizador, Cliente
from flask_login import LoginManager, login_user
from functools import wraps
from flask_login import login_user, current_user, login_required
from functools import wraps
from flask import render_template
from loja import app, db
from werkzeug.security import generate_password_hash


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Favor fazer seu login no sistema primeiro', 'danger')
            return redirect(url_for('login'))
        
        if current_user.roleId != 1:
            flash('Você não tem permissão para acessar esta página', 'danger')
            return redirect(url_for('home')) 
        
        return f(*args, **kwargs)
    
    return decorated_function

@app.route('/')
def layout():
    return render_template('layouts.html')

@app.route('/home')
@login_required
def home():
    return render_template('admin/home.html')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin/index.html', title='Página Administrativa')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilizador.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin'))  # Redireciona para a página de administração
        flash('Email ou senha inválidos', 'danger')
    return render_template('admin/login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Verifica se o papel padrão (role) existe
        role = Role.query.filter_by(id=2).first()
        if not role:
            role = Role(id=2, descricao='Default Role')
            db.session.add(role)
            db.session.commit()
        
        # Cria um novo usuário (Utilizador)
        new_user = Utilizador(
            email=form.email.data,
            roleId=2  # Associando ao papel padrão (role)
        )
        new_user.set_password(form.password.data)  # Define a senha utilizando pbkdf2:sha256
        db.session.add(new_user)
        db.session.commit()
        
        # Cria um novo cliente associado ao usuário
        new_cliente = Cliente(
            nome=form.nome.data,
            morada=form.morada.data,
            utilizadorId=new_user.id
        )
        db.session.add(new_cliente)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    
    return render_template('admin/registrar.html', form=form)

# Método para definir a senha com hash seguro
def set_password(self, password):
    self.password = generate_password_hash(password, method='pbkdf2:sha256')

# Adiciona o método set_password à classe Utilizador
Utilizador.set_password = set_password