from faker import Faker
import random

# Inicializando o gerador de dados fictícios
faker = Faker('pt_BR')  # Especifica que queremos dados em português brasileiro

def gerar_dados_usuarios(num_usuarios):
    usuarios = []
    for _ in range(num_usuarios):
        nome_usuario = faker.name()
        cpf = gerar_cpf()  # Gera um CPF válido
        email = faker.email()
        telefone = gerar_telefone()  # Gera um telefone de Sorocaba
        
        usuarios.append((nome_usuario, cpf, email, telefone))
    
    return usuarios

def gerar_cpf():
    """Gera um CPF válido com pontuação"""
    cpf = [random.randint(0, 9) for _ in range(9)]
    for i in range(2):
        soma = sum(cpf[j] * (10 + i - j) for j in range(9 + i))
        digito = (soma * 10) % 11
        digito = digito if digito < 10 else 0
        cpf.append(digito)
    
    # Formata o CPF com pontuação
    cpf_formatado = f"{''.join(map(str, cpf[:3]))}.{''.join(map(str, cpf[3:6]))}.{''.join(map(str, cpf[6:9]))}-{''.join(map(str, cpf[9:]))}"
    return cpf_formatado

def gerar_telefone():
    """Gera um telefone no formato de Sorocaba"""
    tipo_telefone = random.choice(['fixo', 'celular'])
    ddd = '15'  # DDD de Sorocaba
    if tipo_telefone == 'celular':
        numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    else:
        numero = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    return f"({ddd}) {numero}"

def formatar_sql(usuarios):
    comandos_sql = []
    for usuario in usuarios:
        comando = f"INSERT INTO Usuarios (NomeUsuario, CPF, Email, Telefone) VALUES ('{usuario[0]}', '{usuario[1]}', '{usuario[2]}', '{usuario[3]}');"
        comandos_sql.append(comando)
    return comandos_sql

# Gerando 10 usuários
num_usuarios = 2800
dados_usuarios = gerar_dados_usuarios(num_usuarios)
comandos_sql = formatar_sql(dados_usuarios)

# Salvando os comandos SQL em um arquivo
nome_arquivo = "comandos_sql.txt"
with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
    for comando in comandos_sql:
        arquivo.write(comando + "\n")

print(f"Comandos SQL gerados e salvos em '{nome_arquivo}'.")