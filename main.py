from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
import os
import pandas as pd
import csv
import plotly.io as pio
import hashlib
import datetime
import conexao
app = Flask(__name__)

# Chave secreta para proteger as sessões do Flask
# Clave secreta para proteger las sesiones de Flask
# Secret key to protect Flask's sessions
app.secret_key = "15be550cae6051d0318d82bd5b2dbe8d6f54c0ecd8c93b31"

# Configuração da URI do banco de dados
# Ajustes de la URI de la base de datos
# URI settings from the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/projeto_integrador'

# Inicialização do SQLAlchemy
# Inicialización de SQLAlchemy
# SQLAlchemy Initialization
db = SQLAlchemy(app)

# Definição das classes de modelo
# Definición de clases de modelo
# Defining model classes
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
# Función para hash de la contraseña del usuario
# Function to hash the user's password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Funções CRUD para a entidade de usuário
# Funciones CRUD para la entidad de usuario
# CRUD functions for the user entity
def criar_usuario(name, email, password):
    hashed_password = hash_password(password)
    novo_usuario = User(name=name, email=email, password=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()

def ler_usuario_por_nome(name):
    return User.query.filter_by(name=name).first()

def autenticar_usuario(name, password):
    usuario = ler_usuario_por_nome(name)
    if usuario and usuario.password == hash_password(password):
        return usuario
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    # Verifica se o usuário está autenticado
    # Comprobar si el usuario está autenticado
    # Check if the user is authenticated
    if 'name' not in session:
        return redirect(url_for('login'))
    
    # Consulta despesas do usuário logado
    # Consultar gastos del usuario que ha iniciado sesión.
    # Query expenses of the logged in user
    expenses = Expense.query.filter_by(user_id=session['user_id']).all()

    # Extrai informações relevantes de cada objeto de despesa
    # Extraer información relevante de cada objeto de Gasto
    # Extract relevant information from each Expense object
    expense_data = [{'expense_id': expense.expense_id,
                     'description': expense.description,
                     'value': float(expense.value),
                     'date': expense.date,
                     'category': expense.category,
                     'payment_method': expense.payment_method} for expense in expenses]

    incomes = Income.query.filter_by(user_id=session['user_id']).all()
    
    income_data = [{'income_id' : income.income_id,
                    'description' : income.description,
                    'value' : float(income.value),
                    'date' : income.date,
                    'source' : income.source} for income in incomes]
    
    # Consulta orçamentos do usuário logado
    # Consultar presupuestos del usuario que ha iniciado sesión
    # Query budgets from the logged in user
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    categories = [budget.category for budget in budgets]
    spending_limits = [budget.spending_limit for budget in budgets]   
    graph_html = renderizar_grafico()
    
    return render_template('index.html', expenses=expense_data, incomes = income_data, budgets=budgets, graph_html=graph_html)


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
        usuario = autenticar_usuario(name, password)
        if usuario:
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
    # Remove a chave 'name' da sessão, encerrando a sessão do usuário
    session.pop('name', None)
    session.pop('user_id', None)
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

# Rota para excluir renda
@app.route('/delete_income/<int:income_id>', methods=['POST'])
def delete_income(income_id):
    if 'name' not in session:
        return redirect(url_for('login'))

    # Verifica se a renda pertence ao usuário logado
    income = Income.query.filter_by(income_id=income_id, user_id=session['user_id']).first()
    if not income:
        return redirect(url_for('index'))  # Redireciona se a renda não existir ou não pertencer ao usuário

    # Remove a renda do banco de dados
    db.session.delete(income)
    db.session.commit()

    return redirect(url_for('index'))

# Rota para excluir orçamento
@app.route('/delete_budget/<int:budget_id>', methods=['POST'])
def delete_budget(budget_id):
    if 'name' not in session:
        return redirect(url_for('login'))

    # Verifica se o orçamento pertence ao usuário logado
    budget = Budget.query.filter_by(budget_id=budget_id, user_id=session['user_id']).first()
    if not budget:
        return redirect(url_for('index'))  # Redireciona se o orçamento não existir ou não pertencer ao usuário

    # Remove o orçamento do banco de dados
    db.session.delete(budget)
    db.session.commit()

    return redirect(url_for('index'))

def renderizar_grafico():
    # Consulta despesas, orçamentos e receitas do usuário logado
    expenses = Expense.query.filter_by(user_id=session['user_id']).all()
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    incomes = Income.query.filter_by(user_id=session['user_id']).all()

    # Extrai informações relevantes de cada objeto
    expense_data = sum(expense.value for expense in expenses)
    budget_data = sum(budget.spending_limit for budget in budgets)
    income_data = sum(income.value for income in incomes)

    # Definição de cores amigáveis para daltônicos
    colors = ['#FF5733', '#28A745', '#3399FF']

    # Cria um gráfico de rosca
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=['Despesas', 'Orçamentos', 'Receitas'],
                         values=[expense_data, budget_data, income_data],
                         hole=0.3,
                         marker=dict(colors=colors)))

    # Converte o gráfico para HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html

# Rota para baixar os dados em formato CSV
@app.route('/download_data', methods=['GET'])
def download_data():
    # Consulta despesas, orçamentos e receitas do usuário logado
    expenses = Expense.query.filter_by(user_id=session['user_id']).all()
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    incomes = Income.query.filter_by(user_id=session['user_id']).all()

    # Extrai informações relevantes de cada objeto
    expense_data = [{'Description': expense.description,
                     'Value': float(expense.value),
                     'Date': expense.date,
                     'Category': expense.category,
                     'Payment Method': expense.payment_method} for expense in expenses]

    budget_data = [{'Category': budget.category,
                    'Spending Limit': float(budget.spending_limit),
                    'Period': budget.period} for budget in budgets]

    income_data = [{'Description': income.description,
                    'Value': float(income.value),
                    'Date': income.date,
                    'Source': income.source} for income in incomes]

    # Define os cabeçalhos para o arquivo CSV
    csv_columns = ['Description', 'Value', 'Date', 'Category', 'Payment Method']
    csv_budget_columns = ['Category', 'Spending Limit', 'Period']
    csv_income_columns = ['Description', 'Value', 'Date', 'Source']

    # Cria o arquivo CSV
    csv_data = []
    csv_data.append(csv_columns)
    for row in expense_data:
        csv_data.append([row[col] for col in csv_columns])
    for row in budget_data:
        csv_data.append([row[col] for col in csv_budget_columns])
    for row in income_data:
        csv_data.append([row[col] for col in csv_income_columns])

    # Transforma os dados em formato de lista de listas para uma lista de strings, onde cada string representa uma linha do CSV
    csv_data = [','.join(map(str, row)) for row in csv_data]

    # Cria a resposta CSV
    response = make_response('\n'.join(csv_data))
    response.headers["Content-Disposition"] = "attachment; filename=financas.csv"

    return response

@app.route('/download_data_xlsx', methods=['GET'])
def download_data_xlsx():
    # Consulta despesas, orçamentos e receitas do usuário logado
    expenses = Expense.query.filter_by(user_id=session['user_id']).all()
    budgets = Budget.query.filter_by(user_id=session['user_id']).all()
    incomes = Income.query.filter_by(user_id=session['user_id']).all()

    # Extrai informações relevantes de cada objeto
    expense_data = [{'Description': expense.description,
                     'Value': float(expense.value),
                     'Date': expense.date,
                     'Category': expense.category,
                     'Payment Method': expense.payment_method} for expense in expenses]

    budget_data = [{'Category': budget.category,
                    'Spending Limit': float(budget.spending_limit),
                    'Period': budget.period} for budget in budgets]

    income_data = [{'Description': income.description,
                    'Value': float(income.value),
                    'Date': income.date,
                    'Source': income.source} for income in incomes]

    # Cria DataFrames do pandas com os dados
    df_expenses = pd.DataFrame(expense_data)
    df_budgets = pd.DataFrame(budget_data)
    df_incomes = pd.DataFrame(income_data)

    # Cria um objeto ExcelWriter
    writer = pd.ExcelWriter('financas.xlsx', engine='xlsxwriter')

    # Escreve os DataFrames em diferentes planilhas do arquivo Excel
    df_expenses.to_excel(writer, sheet_name='Despesas', index=False)
    df_budgets.to_excel(writer, sheet_name='Orçamentos', index=False)
    df_incomes.to_excel(writer, sheet_name='Receitas', index=False)

    # Fecha o objeto ExcelWriter
    writer._save()

    # Cria a resposta para download do arquivo Excel
    response = make_response(open('financas.xlsx', 'rb').read())
    response.headers["Content-Disposition"] = "attachment; filename=financas.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return response

if __name__ == '__main__':
    app.run(debug=True)
