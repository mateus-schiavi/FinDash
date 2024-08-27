Documentação do Sistema de Gestão Financeira com Flask

Visão Geral: <br />
Este sistema é uma aplicação web desenvolvida em Flask para gerenciar receitas, despesas e orçamentos pessoais.<br /> Os usuários podem se registrar, fazer login, adicionar e visualizar suas finanças, e acompanhar seus gastos e receitas através de gráficos gerados automaticamente.

Estrutura do Projeto: <br />
Dependências <br />
Flask: Framework web para Python. <br /> 
SQLAlchemy: ORM (Object-Relational Mapping) para interação com o banco de dados. <br />
Plotly: Biblioteca de visualização para gerar gráficos. <br />
Pandas: Usado para manipulação de dados, principalmente no contexto da geração de gráficos. <br />
Configurações: <br />
app.secret_key: Chave secreta para proteger as sessões do Flask. <br />
app.config['SQLALCHEMY_DATABASE_URI']: Configuração da URI para conexão com o banco de dados MySQL. <br />
Modelos de Dados
Classe User
Tabela: users

user_id: Identificador único do usuário (chave primária).
name: Nome do usuário.
email: Endereço de email do usuário.
password: Senha do usuário (armazenada como hash).
registration_date: Data de registro do usuário.
Classe Expense
Tabela: expenses

expense_id: Identificador único da despesa (chave primária).
user_id: Identificador do usuário que cadastrou a despesa (chave estrangeira).
description: Descrição da despesa.
value: Valor da despesa.
date: Data da despesa.
category: Categoria da despesa.
payment_method: Método de pagamento utilizado.
Classe Income
Tabela: income

income_id: Identificador único da receita (chave primária).
user_id: Identificador do usuário que cadastrou a receita (chave estrangeira).
description: Descrição da receita.
value: Valor da receita.
date: Data da receita.
source: Fonte da receita.
Classe Budget
Tabela: budgets

budget_id: Identificador único do orçamento (chave primária).
user_id: Identificador do usuário que cadastrou o orçamento (chave estrangeira).
category: Categoria do orçamento.
spending_limit: Limite de gastos definido para a categoria.
period: Período para o qual o orçamento é válido.
Funções Utilitárias
hash_password(password)
Recebe a senha do usuário, aplica uma função hash SHA-256 e retorna o hash resultante. É utilizada para armazenar senhas de forma segura no banco de dados.

Funções CRUD
criar_usuario(name, email, password)
Cria um novo usuário no banco de dados com os dados fornecidos.

ler_usuario_por_nome(name)
Busca um usuário no banco de dados pelo nome.

autenticar_usuario(name, password)
Autentica um usuário verificando se a senha fornecida corresponde ao hash armazenado.

Rotas
/ (Index)
Métodos: GET, POST
Descrição: Página principal do sistema. Exibe as receitas, despesas e orçamentos do usuário logado, além de um gráfico ilustrando as finanças.
Ações: Requer autenticação. Redireciona para a página de login se o usuário não estiver logado.
/login
Métodos: GET, POST
Descrição: Página de login para autenticação de usuários.
Ações: Se o usuário já estiver logado, redireciona para a página principal. Caso contrário, verifica as credenciais e, se corretas, autentica o usuário.
/reset_password
Métodos: GET, POST
Descrição: Página para redefinição de senha. Permite que o usuário insira uma nova senha, que é então atualizada no banco de dados.
Ações: Verifica se o nome de usuário existe e atualiza a senha.
/register
Métodos: GET, POST
Descrição: Página de registro para novos usuários.
Ações: Verifica se o nome de usuário já existe. Se não, cria uma nova conta de usuário e redireciona para a página de login.
/logout
Métodos: POST
Descrição: Rota para logout. Encerra a sessão do usuário e redireciona para a página de login.
/add_income
Métodos: POST
Descrição: Rota para adicionar uma nova receita ao sistema.
Ações: Adiciona a receita ao banco de dados e redireciona para a página principal.
/add_expense
Métodos: POST
Descrição: Rota para adicionar uma nova despesa ao sistema.
Ações: Adiciona a despesa ao banco de dados e redireciona para a página principal.
/add_budget
Métodos: POST
Descrição: Rota para adicionar um novo orçamento ao sistema.
Ações: Adiciona o orçamento ao banco de dados e redireciona para a página principal.
/delete_expense/<int:expense_id>
Métodos: POST
Descrição: Rota para excluir uma despesa existente.
Ações: Verifica se a despesa pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.
/delete_income/<int:income_id>
Métodos: POST
Descrição: Rota para excluir uma receita existente.
Ações: Verifica se a receita pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.
/delete_budget/<int:budget_id>
Métodos: POST
Descrição: Rota para excluir um orçamento existente.
Ações: Verifica se o orçamento pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.
Funções de Visualização
renderizar_grafico()
Descrição: Gera um gráfico ilustrando as finanças do usuário (despesas, receitas e orçamentos) utilizando a biblioteca Plotly. Retorna o HTML do gráfico para ser embutido na página principal.
Layout e Templates
Os templates HTML utilizados são renderizados com o Flask e podem ser customizados conforme necessário. As rotas que renderizam templates incluem:

login.html
register.html
reset_password.html
index.html
Cada template HTML é responsável por apresentar a interface correspondente, como formulários de login/registro, tabelas de receitas/despesas, e a visualização gráfica das finanças.

Segurança
Senhas: As senhas dos usuários são armazenadas de forma segura no banco de dados utilizando hashing SHA-256.
Sessões: As sessões de usuário são protegidas pela chave secreta do Flask, app.secret_key.
Como Executar
Certifique-se de que o MySQL está instalado e rodando.
Configure o banco de dados e ajuste a URI no app.config['SQLALCHEMY_DATABASE_URI'].
Instale as dependências utilizando pip install -r requirements.txt.
Execute a aplicação com flask run.