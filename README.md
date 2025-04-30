
# 💼 Projeto Integrador - DRP01-PJI110-SALA-001GRUPO-001

## 💡 Visão Geral

O presente projeto tem como objetivo o desenvolvimento de uma **Aplicação Web de Gestão Financeira Pessoal**, elaborada como parte do Projeto Integrador do curso de **Engenharia da Computação da UNIVESP**.

A proposta consiste em ajudar os usuários a acompanhar suas **receitas, despesas e orçamentos**, com armazenamento seguro dos dados em um banco de dados MySQL e uso de controle de versão para rastrear alterações nos registros financeiros. A aplicação conta com autenticação de usuários e interface de visualização via gráficos interativos.

---

## 👥 Integrantes do Grupo

- Alexandre Luiz Alonso  
- Cassia Conceição da Silva  
- Elisete Magalhães da Silva  
- Luis Henrique Ponciano Marques de Oliveira  
- Mateus de Sousa Schiavi  
- Rafael Marcos Batista dos Santos  
- Rafael Paoleschi Iurovschi  

---

## ⚙️ Tecnologias Utilizadas

- **Flask** – Framework web para Python  
- **SQLAlchemy** – ORM para banco de dados  
- **MySQL** – Banco relacional usado como persistência  
- **Pandas** – Manipulação e análise de dados  
- **Plotly** – Geração de gráficos interativos  
- **HTML + CSS + Jinja2** – Templates renderizados no servidor  

---

## 📐 Estrutura de Dados

### 📄 Classe `User` (Tabela: `users`)
- `user_id` (PK): ID do usuário  
- `name`: Nome  
- `email`: E-mail  
- `password`: Senha criptografada (SHA-256)  
- `registration_date`: Data de registro  

### 📄 Classe `Expense` (Tabela: `expenses`)
- `expense_id` (PK): ID da despesa  
- `user_id` (FK): ID do usuário  
- `description`, `value`, `date`, `category`, `payment_method`  

### 📄 Classe `Income` (Tabela: `income`)
- `income_id` (PK): ID da receita  
- `user_id` (FK): ID do usuário  
- `description`, `value`, `date`, `source`  

### 📄 Classe `Budget` (Tabela: `budgets`)
- `budget_id` (PK): ID do orçamento  
- `user_id` (FK): ID do usuário  
- `category`, `spending_limit`, `period`  

---

## 🔐 Funções de Segurança

- `hash_password(password)`: Aplica SHA-256 à senha  
- Sessões protegidas por `app.secret_key`  
- Verificações de permissão em ações de CRUD  

---

## 🔄 Rotas da Aplicação

| Rota                        | Método | Descrição                                                                 |
|-----------------------------|--------|---------------------------------------------------------------------------|
| `/`                         | GET/POST | Página principal com resumo e gráfico                                     |
| `/login`                    | GET/POST | Login de usuários                                                         |
| `/register`                 | GET/POST | Registro de novos usuários                                                |
| `/reset_password`           | GET/POST | Redefinição de senha                                                      |
| `/logout`                   | POST     | Logout do usuário                                                         |
| `/add_income`               | POST     | Adicionar receita                                                         |
| `/add_expense`              | POST     | Adicionar despesa                                                         |
| `/add_budget`               | POST     | Adicionar orçamento                                                       |
| `/delete_income/<id>`       | POST     | Excluir receita                                                           |
| `/delete_expense/<id>`      | POST     | Excluir despesa                                                           |
| `/delete_budget/<id>`       | POST     | Excluir orçamento                                                         |

---

## 📊 Visualização de Dados

A função `renderizar_grafico()` gera um gráfico dinâmico usando **Plotly**, exibindo um resumo visual das receitas, despesas e orçamentos do usuário. O gráfico é incorporado diretamente na **página principal** (`index.html`).

---

## 🖼️ Templates HTML

Os templates da aplicação incluem:

- `login.html`: Tela de login  
- `register.html`: Registro de novos usuários  
- `reset_password.html`: Redefinir senha  
- `index.html`: Painel financeiro com dados e gráficos  

---

## 🧪 Execução do Projeto

1. Verifique se o MySQL está instalado e em execução.
2. Clone o projeto:
```bash
git clone https://github.com/mateus-schiavi/PI-Univesp.git
cd PI-Univesp
```
3. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS  
venv\Scripts\activate         # Windows
```
4. Instale as dependências:
```bash
pip install -r requirements.txt
```
5. Configure a URI do banco de dados no `main.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@localhost/nome_do_banco'
```
6. Execute a aplicação:
```bash
python main.py
```
7. Acesse via navegador:
```
http://127.0.0.1:5000
```

---

## 🏁 Considerações Finais

Este projeto acadêmico foi idealizado para consolidar conhecimentos de **programação back-end**, **persistência de dados**, **segurança de sistemas web**, e **visualização interativa de informações financeiras**, integrando teoria e prática com foco em aplicações reais.
