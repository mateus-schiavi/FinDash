from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import pandas as pd
import hashlib
import datetime
from conexao import conn

app = Flask(__name__)

# Chave secreta para proteger as sessões do Flask
app.secret_key = "sua_chave_secreta"

# Configuração da URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/projeto_integrador'

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Remember to encrypt the password before storing it in the database
    registration_date = db.Column(db.Date, nullable=False, default=datetime.utcnow())

class Expense(db.Model):
    __tablename__ = 'expenses'
    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.user_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))

class Income(db.Model):
    __tablename__ = 'income'
    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.user_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100))

class Budget(db.Model):
    __tablename__ = 'budget'
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.user_id'), nullable=False)
    category = db.Column(db.String(100))
    spending_limit = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(50))


# DataFrame para armazenar os dados financeiros
data = {
    'Date': pd.date_range(start='2024-01-01', periods=10),
    'Revenue': [100, 110, 120, 130, 140, 150, 160, 170, 180, 190],
    'Expenses': [80, 85, 90, 95, 100, 105, 110, 115, 120, 125]
}
df = pd.DataFrame(data)

# Função para hashear a senha do usuário
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Rota principal que exibe o dashboard financeiro
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifica se o usuário está autenticado
    if 'name' not in session:
        return redirect(url_for('login'))
    
    # Manipula os dados enviados pelo formulário
    if request.method == 'POST':
        revenue = float(request.form['revenue'])
        expenses = float(request.form['expenses'])
        new_data = {'Date': pd.Timestamp.now(), 'Revenue': revenue, 'Expenses': expenses}
        df.loc[len(df)] = new_data

    # Cria visualização Plotly do dashboard
    fig = px.line(df, x='Date', y=['Revenue', 'Expenses'], title='Finance Dashboard')
    graph_html = fig.to_html(full_html=False)

    # Renderiza o template HTML do dashboard
    return render_template('index.html', graph_html=graph_html)

# Rota de login para autenticar os usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifica se o usuário já está autenticado
    if 'name' in session:
        return redirect(url_for('index'))
    
    # Manipula os dados enviados pelo formulário de login
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = hash_password(password)
        user = User.query.filter_by(name=name).first()
        if user and user.password == hashed_password:
            # Autentica o usuário e redireciona para o dashboard
            session['name'] = name
            return redirect(url_for('index'))
        else:
            # Exibe mensagem de erro se as credenciais forem inválidas
            return render_template('login.html', error='Invalid name or password')
    else:
        # Renderiza o template HTML da página de login
        return render_template('login.html', error='')

# Rota de registro para criar novas contas de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Verifica se o usuário já está autenticado
    if 'name' in session:
        return redirect(url_for('index'))
    
    # Manipula os dados enviados pelo formulário de registro
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = hash_password(password)
        if not User.query.filter_by(name=name).first():
            # Cria um novo usuário no banco de dados
            new_user = User(name=name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # Exibe mensagem de erro se o nome de usuário já existe
            return render_template('register.html', error='name already exists')
    else:
        # Renderiza o template HTML da página de registro
        return render_template('register.html', error='')

@app.route('/logout', methods=['POST'])
def logout():
    # Remove a chave 'name' da sessão, encerrando a sessão do usuário
    session.pop('name', None)
    return redirect(url_for('login'))


# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
