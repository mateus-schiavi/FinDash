import mysql.connector

try:
    # Estabelecer a conexão com o banco de dados
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projeto_integrador"
    )

    if conexao.is_connected():
        print("Conexão bem-sucedida ao banco de dados!")

except mysql.connector.Error as erro:
    print("Erro ao conectar ao banco de dados:", erro)

finally:
    # Fechar a conexão
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
        print("Conexão fechada.")
