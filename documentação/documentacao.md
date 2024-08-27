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
Modelos de Dados <br />
Classe User <br />
Tabela: users <br />

user_id: Identificador único do usuário (chave primária). <br />
name: Nome do usuário. <br />
email: Endereço de email do usuário. <br />
password: Senha do usuário (armazenada como hash). <br />
registration_date: Data de registro do usuário. <br />
Classe Expense <br />
Tabela: expenses <br />

expense_id: Identificador único da despesa (chave primária). <br />
user_id: Identificador do usuário que cadastrou a despesa (chave estrangeira). <br />
description: Descrição da despesa. <br />
value: Valor da despesa. <br />
date: Data da despesa. <br />
category: Categoria da despesa. <br />
payment_method: Método de pagamento utilizado. <br />
Classe Income <br />
Tabela: income <br />

income_id: Identificador único da receita (chave primária). <br />
user_id: Identificador do usuário que cadastrou a receita (chave estrangeira).<br />
description: Descrição da receita.<br />
value: Valor da receita.<br />
date: Data da receita.<br />
source: Fonte da receita.<br />
Classe Budget<br />
Tabela: budgets<br />

budget_id: Identificador único do orçamento (chave primária).<br />
user_id: Identificador do usuário que cadastrou o orçamento (chave estrangeira).<br />
category: Categoria do orçamento.<br />
spending_limit: Limite de gastos definido para a categoria.<br />
period: Período para o qual o orçamento é válido.<br />
Funções Utilitárias<br />
hash_password(password)<br />
Recebe a senha do usuário, aplica uma função hash SHA-256 e retorna o hash resultante.<br /> É utilizada para armazenar senhas de forma segura no banco de dados.

Funções CRUD<br />
criar_usuario(name, email, password)<br />
Cria um novo usuário no banco de dados com os dados fornecidos.<br />

ler_usuario_por_nome(name) <br />
Busca um usuário no banco de dados pelo nome.<br />

autenticar_usuario(name, password)<br />
Autentica um usuário verificando se a senha fornecida corresponde ao hash armazenado.<br />

Rotas: <br />
/ (Index)<br />
Métodos: GET, POST<br />
Descrição: Página principal do sistema. Exibe as receitas, despesas e orçamentos do usuário logado, além de um gráfico ilustrando as finanças. <br />
Ações:<br />
Requer autenticação.<br /> Redireciona para a página de login se o usuário não estiver logado.
/login <br />
Métodos: <br />
GET, POST<br />
Descrição:<br/> Página de login para autenticação de usuários. <br/>
Ações:<br/> Se o usuário já estiver logado, redireciona para a página principal. <br/> Caso contrário, verifica as credenciais e, se corretas, autentica o usuário.
/reset_password<br/>
Métodos:<br/> GET, POST<br/>
Descrição: <br/>Página para redefinição de senha.<br/> Permite que o usuário insira uma nova senha, que é então atualizada no banco de dados.
Ações:<br/> Verifica se o nome de usuário existe e atualiza a senha.<br/>
/register<br/>
Métodos:<br/> GET, POST<br/>
Descrição:<br/> Página de registro para novos usuários.<br/>
Ações:<br/> Verifica se o nome de usuário já existe. <br/>Se não, cria uma nova conta de usuário e redireciona para a página de login.<br/>
/logout<br/>
Métodos:<br/> POST<br/>
Descrição: <br/>Rota para logout. <br/>Encerra a sessão do usuário e redireciona para a página de login.
/add_income<br/>
Métodos:<br/> POST<br/>
Descrição:<br/> Rota para adicionar uma nova receita ao sistema.
Ações:<br/> Adiciona a receita ao banco de dados e redireciona para a página principal.
/add_expense<br/>
Métodos: POST<br/>
Descrição:<br/> Rota para adicionar uma nova despesa ao sistema.<br/>
Ações:<br/> Adiciona a despesa ao banco de dados e redireciona para a página principal.
/add_budget<br/>
Métodos:<br/> POST<br/>
Descrição:<br/> Rota para adicionar um novo orçamento ao sistema.
Ações:<br/> Adiciona o orçamento ao banco de dados e redireciona para a página principal.<br/>
/delete_expense/<int:expense_id><br/>
Métodos: <br/>POST<br/>
Descrição:<br/> Rota para excluir uma despesa existente.<br/>
Ações:<br/> Verifica se a despesa pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.<br/>
/delete_income/<int:income_id><br/>
Métodos:<br/> POST<br/>
Descrição: <br/>Rota para excluir uma receita existente.
Ações: <br/>Verifica se a receita pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.<br/>
/delete_budget/<int:budget_id><br/>
Métodos:<br/> POST<br/>
Descrição:<br/> Rota para excluir um orçamento existente.
Ações:<br/> Verifica se o orçamento pertence ao usuário logado, remove do banco de dados e redireciona para a página principal.<br/>
Funções de Visualização<br/>
renderizar_grafico()<br/>
Descrição:<br/> Gera um gráfico ilustrando as finanças do usuário (despesas, receitas e orçamentos) utilizando a biblioteca Plotly.<br/> Retorna o HTML do gráfico para ser embutido na página principal.
Layout e Templates<br/>
Os templates HTML utilizados são renderizados com o Flask e podem ser customizados conforme necessário.<br/> As rotas que renderizam templates incluem:

login.html<br/>
register.html<br/>
reset_password.html<br/>
index.html<br/>
Cada template HTML é responsável por apresentar a interface correspondente, como formulários de login/registro, tabelas de receitas/despesas, e a visualização gráfica das finanças.<br/>

Segurança<br/>
Senhas:<br/> As senhas dos usuários são armazenadas de forma segura no banco de dados utilizando hashing SHA-256.
Sessões:<br/> As sessões de usuário são protegidas pela chave secreta do Flask, app.secret_key.
Como Executar<br/>
Certifique-se de que o MySQL está instalado e rodando.<br/>
Configure o banco de dados e ajuste a URI no app.config['SQLALCHEMY_DATABASE_URI'].<br/>
Verifique as dependências utilizando pip install -r requirements.txt.<br/>
Instale as dependências utilizando o comando pip install + nome da biblioteca.<br />
Por exemplo: se for instalar Flask, o comando é pip install Flask.<br />
Execute a aplicação com python main.py.<br/>