import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect(r'D:\Bruno\FATEC CDN\ProjetoIntegrador2\FinanceiroQuadraGo\DB_Config\FinanceiroQuadraGo.db')
cursor = conn.cursor()

# Obter as reservas com seus pagamentos
cursor.execute('''
    SELECT r.ID_Reserva, p.ID_Pagamento, p.DataPagamento, p.Valor, f.Taxa 
    FROM Reservas r
    JOIN Pagamento p ON r.ID_Reserva = p.ID_Reserva
    JOIN FormasPagamento f ON p.ID_FormaPagamento = f.ID_FormaPagamento
''')
reservas_pagamentos = cursor.fetchall()

# Preparar os dados de receitas
receitas = []
for reserva in reservas_pagamentos:
    id_reserva, id_pagamento, data_pagamento, valor_pago, taxa_transacao = reserva
    valor_receita = valor_pago * (1 - taxa_transacao)  # Calcula o valor da receita descontando a taxa
    origem_receita = "Reserva"  # Neste caso, a origem é sempre 'Reserva'
    
    receitas.append((id_pagamento, data_pagamento, origem_receita, valor_receita))

# Inserir receitas na tabela Receitas
cursor.executemany('''
    INSERT INTO Receitas (
        ID_Pagamento,
        DataReceita,
        OrigemReceita,
        ValorReceita
    ) VALUES (?, ?, ?, ?)
''', receitas)

# Confirmar e fechar conexão
conn.commit()
conn.close()
print(f"{len(receitas)} receitas inseridas com sucesso!")
