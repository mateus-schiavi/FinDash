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
    value = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))

class Income(db.Model):
    __tablename__ = 'income'
    income_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Numeric(10, 2), nullable=False)
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

# Funções CRUD para a entidade de usuário
def criar_usuario(name, email, password):
    hashed_password = hash_password(password)
    novo_usuario = User(name=name, email=email, password=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()

def ler_usuario_por_id(user_id):
    usuario = User.query.get(user_id)
    return usuario

def ler_usuario_por_nome(name):
    usuario = User.query.filter_by(name=name).first()
    return usuario

def atualizar_usuario(user_id, name, email, password):
    usuario = User.query.get(user_id)
    usuario.name = name
    usuario.email = email
    usuario.password = hash_password(password)
    db.session.commit()

def excluir_usuario(user_id):
    usuario = User.query.get(user_id)
    db.session.delete(usuario)
    db.session.commit()

# Rota principal que exibe o dashboard financeiro
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifica se o usuário está autenticado
    if 'name' not in session:
        return redirect(url_for('login'))
    
    # Consulta despesas do usuário logado
    expenses = Expense.query.filter_by(user_id=session['user_id']).all()

    # Consulta orçamentos do usuário logado
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    categories = [budget.category for budget in budgets]
    spending_limits = [budget.spending_limit for budget in budgets]

    # Define as cores para cada tipo de dado
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Azul, laranja e verde

    # Cria um gráfico com 3 séries de pontos para despesas, orçamento e receitas
    fig = go.Figure()

    # Adiciona uma série de pontos para despesas
    fig.add_trace(go.Scatter(x=categories, y=spending_limits, mode='markers', name='Despesas', marker=dict(color=colors[0], size=10)))

    # Adiciona uma série de pontos para o orçamento (apenas para demonstração, ajuste conforme necessário)
    fig.add_trace(go.Scatter(x=categories, y=[1000]*len(categories), mode='markers', name='Orçamento', marker=dict(color=colors[1], size=10)))

    # Adiciona uma série de pontos para receitas (apenas para demonstração, ajuste conforme necessário)
    fig.add_trace(go.Scatter(x=categories, y=[800]*len(categories), mode='markers', name='Receitas', marker=dict(color=colors[2], size=10)))

    # Define layout do gráfico
    fig.update_layout(title='Dashboard Financeiro',
                      xaxis_title='Categoria',
                      yaxis_title='Valor')

    # Converte o gráfico para HTML
    graph_html = fig.to_html(full_html=False)

    # Renderiza o template HTML do dashboard, passando os dados do gráfico e das despesas
    return render_template('index.html', graph_html=graph_html, expenses=expenses)


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
        usuario = ler_usuario_por_nome(name)
        if usuario and usuario.password == hash_password(password):
            # Autentica o usuário e redireciona para o dashboard
            session['name'] = name
            session['user_id'] = usuario.user_id  # Armazena o ID do usuário na sessão
            return redirect(url_for('index'))
        else:
            # Exibe mensagem de erro se as credenciais forem inválidas
            return render_template('login.html', error='Nome ou senha inválidos')
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
        email = request.form['email']
        password = request.form['password']
        if not ler_usuario_por_nome(name):
            # Cria um novo usuário no banco de dados
            criar_usuario(name, email, password)
            return redirect(url_for('login'))
        else:
            # Exibe mensagem de erro se o nome de usuário já existe
            return render_template('register.html', error='Nome de usuário já existe')
    else:
        # Renderiza o template HTML da página de registro
        return render_template('register.html', error='')

# Rota de logout para encerrar a sessão do usuário
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

# Rota para adicionar receita
@app.route('/add_income', methods=['POST'])
def add_income():
    if 'name' not in session:
        return redirect(url_for('login'))

    description = request.form['description']
    value = request.form['value']
    date = request.form['date']
    source = request.form['source']

    new_income = Income(user_id=session['user_id'], description=description, value=value, date=date, source=source)
    db.session.add(new_income)
    db.session.commit()

    return redirect(url_for('index'))

# Rota para adicionar despesa
@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'name' not in session:
        return redirect(url_for('login'))

    description = request.form['description']
    value = request.form['value']
    date = request.form['date']
    category = request.form['category']
    payment_method = request.form['payment_method']

    new_expense = Expense(user_id=session['user_id'], description=description, value=value, date=date, category=category, payment_method=payment_method)
    db.session.add(new_expense)
    db.session.commit()

    return redirect(url_for('index'))

# Rota para adicionar orçamento
@app.route('/add_budget', methods=['POST'])
def add_budget():
    if 'name' not in session:
        return redirect(url_for('login'))

    category = request.form['category']
    spending_limit = request.form['spending_limit']
    period = request.form['period']

    new_budget = Budget(user_id=session['user_id'], category=category, spending_limit=spending_limit, period=period)
    db.session.add(new_budget)
    db.session.commit()

    return redirect(url_for('index'))

# Rota para excluir despesa
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    if 'name' not in session:
        return redirect(url_for('login'))

    # Verifica se a despesa pertence ao usuário logado
    expense = Expense.query.filter_by(expense_id=expense_id, user_id=session['user_id']).first()
    if not expense:
        return redirect(url_for('index'))  # Redireciona se a despesa não existir ou não pertencer ao usuário

    # Remove a despesa do banco de dados
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
