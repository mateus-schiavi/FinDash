import hashlib

def criptografar_senha(senha):
    # Convertendo a senha em bytes
    senha_bytes = senha.encode('utf-8')
    
    # Criando um objeto de hash usando SHA-256
    hash_obj = hashlib.sha256()
    
    # Atualizando o objeto de hash com a senha em bytes
    hash_obj.update(senha_bytes)
    
    # Obtendo o hash criptografado
    senha_criptografada = hash_obj.hexdigest()
    
    return senha_criptografada

# Exemplo de uso
senha = "senha123"
senha_criptografada = criptografar_senha(senha)
print("Senha criptografada:", senha_criptografada)
