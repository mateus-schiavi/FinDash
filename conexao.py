import pymysql

try:
    # Estabelece a conexão com o banco de dados
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="projeto_integrador",
        charset='utf8mb4',  # recomendado
        cursorclass=pymysql.cursors.DictCursor
    )

    # Se a conexão for bem-sucedida, exibe uma mensagem
    print("Conexão bem-sucedida!")

except pymysql.MySQLError as e:
    # Se ocorrer algum erro ao conectar, exibe a mensagem de erro
    print(f"Erro ao conectar: {e}")
