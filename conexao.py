import mysql.connector

try:
    # Estabelece a conexão com o banco de dados
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projeto_integrador"
    )

    # Se a conexão for bem-sucedida, exibe uma mensagem
    print("Conexão bem-sucedida!")

except mysql.connector.Error as e:
    # Se ocorrer algum erro ao conectar, exibe a mensagem de erro
    print(f"Erro ao conectar: {e}")

