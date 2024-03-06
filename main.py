from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
import pandas as pd
import hashlib
import datetime
import conexao


app = Flask(__name__)

# Chave secreta para proteger as sessões do Flask
app.secret_key = "15be550cae6051d0318d82bd5b2dbe8d6f54c0ecd8c93b31"

# Configuração da URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/projeto_integrador'

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Definição das classes de modelo
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.Date, nullable=False, default=datetime.datetime.utcnow())

class Expense(db.Model):
    __tablename__ = 'expenses'
    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))

class Income(db.Model):
    __tablename__ = 'income'
    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100))

class Budget(db.Model):
    __tablename__ = 'budgets'
    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category = db.Column(db.String(100))
    spending_limit = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(50))


# Função para hashear a senha do usuário
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Rota principal que exibe o dashboard financeiro
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifica se o usuário está autenticado
    if 'name' not in session:
        return redirect(url_for('login'))
    
    # Consulta orçamentos do usuário logado
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    categories = [budget.category for budget in budgets]
    spending_limits = [budget.spending_limit for budget in budgets]

    # Define as cores para cada tipo de dado
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Azul, laranja e verde

    # Cria um gráfico com 3 séries de pontos para despesas, orçamento e receitas
    fig = go.Figure()

    # Adiciona uma série de pontos para despesas
    fig.add_trace(go.Scatter(x=categories, y=spending_limits, mode='markers', name='Expenses', marker=dict(color=colors[0], size=10)))

    # Adiciona uma série de pontos para o orçamento (apenas para demonstração, ajuste conforme necessário)
    fig.add_trace(go.Scatter(x=categories, y=[1000]*len(categories), mode='markers', name='Budget', marker=dict(color=colors[1], size=10)))

    # Adiciona uma série de pontos para receitas (apenas para demonstração, ajuste conforme necessário)
    fig.add_trace(go.Scatter(x=categories, y=[800]*len(categories), mode='markers', name='Income', marker=dict(color=colors[2], size=10)))

    # Define layout do gráfico
    fig.update_layout(title='Finance Dashboard',
                      xaxis_title='Category',
                      yaxis_title='Amount')

    # Converte o gráfico para HTML
    graph_html = fig.to_html(full_html=False)

    # Renderiza o template HTML do dashboard, passando os dados do gráfico
    return render_template('index.html', graph_html=graph_html)

# Rota de login para autenticar os usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifica se o usuário já está autenticado
    if 'name' in session:
        return redirect(url_for('index'))
    
    # Manipula os dados enviados pelo formulário de login
    if request.method == 'POST':
        name = request.form['username']  # Alterado para corresponder ao campo 'username' do formulário HTML
        password = request.form['password']
        hashed_password = hash_password(password)
        user = User.query.filter_by(name=name).first()
        if user and user.password == hashed_password:
            # Autentica o usuário e redireciona para o dashboard
            session['name'] = name
            session['user_id'] = user.user_id  # Armazena o ID do usuário na sessão
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
    try:
        # Remove a chave 'name' da sessão, encerrando a sessão do usuário
        session.pop('name')
        session.pop('user_id')  # Remove também o ID do usuário da sessão
    except KeyError:
        # Se a chave 'name' não existir na sessão, não faz nada
        pass
    return redirect(url_for('login'))

# Executa o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
