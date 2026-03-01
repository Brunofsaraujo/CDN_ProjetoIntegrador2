import sqlite3
import random
from datetime import datetime

# Conectar ao banco de dados SQLite
conn = sqlite3.connect(r'D:\Bruno\FATEC CDN\ProjetoIntegrador2\FinanceiroQuadraGo\DB_Config\FinanceiroQuadraGo.db')
cursor = conn.cursor()

# Obter as reservas existentes
cursor.execute("SELECT ID_Reserva, DataReserva, ValorTotal FROM Reservas")
reservas = cursor.fetchall()

# Obter as opções de formas de pagamento
cursor.execute("SELECT ID_FormaPagamento FROM FormasPagamento")
formas_pagamento = [row[0] for row in cursor.fetchall()]

# Função para gerar um pagamento
def gerar_pagamento(id_reserva, valor, data_pagamento):
    id_forma_pagamento = random.choice(formas_pagamento)
    status_pagamento = random.choice(["Pago"])  # Status aleatório
    return (
        id_reserva,
        id_forma_pagamento,
        valor,
        data_pagamento,
        status_pagamento
    )

# Preparar os pagamentos para inserção
pagamentos = []
for reserva in reservas:
    id_reserva, data_reserva, valor_total = reserva
    pagamento = gerar_pagamento(id_reserva, valor_total, data_reserva)
    pagamentos.append(pagamento)

# Inserir pagamentos na tabela Pagamento
cursor.executemany('''
    INSERT INTO Pagamento (
        ID_Reserva,
        ID_FormaPagamento,
        Valor,
        DataPagamento,
        StatusPagamento
    ) VALUES (?, ?, ?, ?, ?)
''', pagamentos)

# Confirmar e fechar conexão
conn.commit()
conn.close()
print(f"{len(pagamentos)} pagamentos inseridos com sucesso!")
