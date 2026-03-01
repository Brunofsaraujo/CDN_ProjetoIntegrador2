import sqlite3
import random
from datetime import datetime, timedelta

# Conectar ao banco de dados SQLite
conn = sqlite3.connect(r'D:\Bruno\FATEC CDN\ProjetoIntegrador2\FinanceiroQuadraGo\DB_Config\FinanceiroQuadraGo.db')
cursor = conn.cursor()

# Obter os IDs das quadras e os respectivos PrecoHora
cursor.execute("SELECT ID_QuadraEsporte, PrecoHora FROM QuadraEsporte")
quadras = {row[0]: row[1] for row in cursor.fetchall()}

# Configurações para geração de reservas
total_reservas = 1850
usuarios_total = 2800
percent_usuarios_recurrentes = 0.8
percent_horarios_nobres = 0.6  # 60% das reservas entre 18h e 22h
horarios_nobres = (18, 22)  # Horário nobre das 18h às 22h
horarios_comuns = (8, 22)  # Horário geral das 8h às 22h

# Função para obter usuários recorrentes a partir do banco de dados
def obter_usuarios_recorrentes():
    cursor.execute("SELECT DISTINCT ID_Usuario FROM Reservas")
    return [row[0] for row in cursor.fetchall()]

# Inicializar a lista de usuários recorrentes a partir do banco de dados
usuarios_recorrentes = obter_usuarios_recorrentes()

# Obter todos os IDs de usuários possíveis
usuarios_disponiveis = list(range(1, usuarios_total + 1))

# Função para gerar uma reserva
def gerar_reserva(quadra_id, usuario_id, data, hora_inicio, hora_fim):
    preco_hora = quadras[quadra_id]
    duracao_horas = (datetime.combine(data, hora_fim) - datetime.combine(data, hora_inicio)).seconds / 3600
    valor_total = round(preco_hora * duracao_horas, 2)  # Calcula o valor total com base na duração e PrecoHora
    status_reserva = random.choice(['Confirmada'])
    quantidade_pessoas = random.randint(2, 10)
    
    return (
        usuario_id,
        quadra_id,
        data,
        hora_inicio.strftime("%H:%M:%S"),
        hora_fim.strftime("%H:%M:%S"),
        valor_total,
        status_reserva,
        quantidade_pessoas
    )

# Listas para controlar as reservas únicas
reservas_existentes = set()
reservas = []

# Gerar as reservas
for _ in range(total_reservas):
    quadra_id = random.choice(list(quadras.keys()))

    # Escolher usuário com base na recorrência desejada
    if random.random() < percent_usuarios_recurrentes and usuarios_recorrentes:
        usuario_id = random.choice(usuarios_recorrentes)
    else:
        usuario_id = random.choice(usuarios_disponiveis)
        usuarios_disponiveis.remove(usuario_id)
        usuarios_recorrentes.append(usuario_id)

    # Gera data aleatória em janeiro de 2026
    data = datetime(2026, 12, random.randint(1, 31))

    # Escolher horário com probabilidade de 60% para horários nobres
    if random.random() < percent_horarios_nobres:
        hora_inicio = random.randint(horarios_nobres[0], horarios_nobres[1] - 1)
    else:
        hora_inicio = random.randint(horarios_comuns[0], horarios_comuns[1] - 1)

    duracao = timedelta(hours=random.randint(1, 3))
    hora_inicio_dt = datetime.combine(data, datetime.min.time()) + timedelta(hours=hora_inicio)
    hora_fim_dt = hora_inicio_dt + duracao

    # Verifica se a quadra já está reservada no intervalo de tempo
    conflito = False
    for (res_quadra_id, res_data, res_hora_inicio, res_hora_fim) in reservas_existentes:
        res_hora_inicio_dt = datetime.combine(res_data, res_hora_inicio)  # Combina data com hora de início
        res_hora_fim_dt = datetime.combine(res_data, res_hora_fim)  # Combina data com hora de fim
        
        if (res_quadra_id == quadra_id and res_data == data.date() and
                not (hora_fim_dt <= res_hora_inicio_dt or hora_inicio_dt >= res_hora_fim_dt)):
            conflito = True
            break

    if conflito:
        continue  # Se já existe reserva, vai para a próxima iteração

    # Adicionar reserva aos dados
    reserva = gerar_reserva(quadra_id, usuario_id, data.date(), hora_inicio_dt.time(), hora_fim_dt.time())
    reservas.append(reserva)
    reservas_existentes.add((quadra_id, data.date(), hora_inicio_dt.time(), hora_fim_dt.time()))

# Inserir reservas na tabela
cursor.executemany('''
    INSERT INTO Reservas (
        ID_Usuario,
        ID_QuadraEsporte,
        DataReserva,
        HoraInicio,
        HoraFim,
        ValorTotal,
        StatusReserva,
        QuantidadePessoas
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', reservas)

# Confirmar e fechar conexão
conn.commit()
conn.close()
print(f"{total_reservas} reservas inseridas com sucesso!")
