# Sistema de Gestão Financeira com Flask

## Visão Geral
O **Sistema de Gestão Financeira** é uma aplicação web desenvolvida em **Flask** para gerenciar receitas, despesas e orçamentos pessoais.  

Principais funcionalidades:  
- Registro e login de usuários  
- Cadastro e visualização de receitas e despesas  
- Criação e gerenciamento de orçamentos  
- Visualização de gráficos financeiros interativos  

---

## Estrutura do Projeto

### Dependências
- **Flask**: Framework web para Python  
- **SQLAlchemy**: ORM para interação com o banco de dados  
- **Plotly**: Biblioteca de visualização para gerar gráficos interativos  
- **Pandas**: Manipulação de dados, principalmente para gráficos  
- **PyMySQL / mysqlclient**: Conexão com o banco de dados MySQL  

### Configurações
- `app.secret_key`: Protege as sessões do Flask  
- `app.config['SQLALCHEMY_DATABASE_URI']`: URI de conexão com o banco de dados MySQL  

---

## Modelos de Dados

### User (`users`)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| user_id | int | Identificador único (PK) |
| name | str | Nome do usuário |
| email | str | Email do usuário |
| password | str | Senha (armazenada como hash) |
| registration_date | datetime | Data de registro |

### Expense (`expenses`)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| expense_id | int | Identificador único (PK) |
| user_id | int | FK do usuário que cadastrou |
| description | str | Descrição da despesa |
| value | float | Valor da despesa |
| date | date | Data da despesa |
| category | str | Categoria da despesa |
| payment_method | str | Método de pagamento |

### Income (`income`)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| income_id | int | Identificador único (PK) |
| user_id | int | FK do usuário que cadastrou |
| description | str | Descrição da receita |
| value | float | Valor da receita |
| date | date | Data da receita |
| source | str | Fonte da receita |

### Budget (`budgets`)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| budget_id | int | Identificador único (PK) |
| user_id | int | FK do usuário que cadastrou |
| category | str | Categoria do orçamento |
| spending_limit | float | Limite de gastos |
| period | str | Período do orçamento |

---

## Funções Utilitárias

### `hash_password(password)`
Aplica hash SHA-256 na senha e retorna o hash.  
Usada para armazenar senhas de forma segura.

---

## Funções CRUD

| Função | Descrição |
|--------|-----------|
| `criar_usuario(name, email, password)` | Cria um novo usuário |
| `ler_usuario_por_nome(name)` | Busca um usuário pelo nome |
| `autenticar_usuario(name, password)` | Verifica se a senha corresponde ao hash |

---

## Rotas

| Rota | Métodos | Descrição |
|------|---------|-----------|
| `/` | GET, POST | Página principal com receitas, despesas, orçamentos e gráficos (requer login) |
| `/login` | GET, POST | Página de login de usuários |
| `/reset_password` | GET, POST | Redefinir senha |
| `/register` | GET, POST | Registrar novo usuário |
| `/logout` | POST | Logout do usuário |
| `/add_income` | POST | Adicionar nova receita |
| `/add_expense` | POST | Adicionar nova despesa |
| `/add_budget` | POST | Adicionar novo orçamento |
| `/delete_expense/<int:expense_id>` | POST | Excluir despesa do usuário logado |
| `/delete_income/<int:income_id>` | POST | Excluir receita do usuário logado |
| `/delete_budget/<int:budget_id>` | POST | Excluir orçamento do usuário logado |

---

## Funções de Visualização

### `renderizar_grafico()`
- Gera gráficos financeiros interativos utilizando **Plotly**  
- Retorna o HTML do gráfico para ser embutido na página principal

---

## Layout e Templates
- **login.html**: Formulário de login  
- **register.html**: Formulário de registro  
- **reset_password.html**: Redefinição de senha  
- **index.html**: Página principal com tabelas e gráficos  

---

## Segurança
- **Senhas**: Hash SHA-256  
- **Sessões**: Protegidas pelo `app.secret_key`  

---

## Como Executar

1. Certifique-se de que o **MySQL** está instalado e rodando  
2. Configure o banco de dados e ajuste a URI em `app.config['SQLALCHEMY_DATABASE_URI']`  
3. Instale as dependências:
```bash
pip install -r requirements.txt
