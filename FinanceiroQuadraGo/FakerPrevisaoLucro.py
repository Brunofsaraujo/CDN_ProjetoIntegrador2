import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Conexão com o banco de dados
conn = sqlite3.connect(r'D:\Bruno\FATEC CDN\ProjetoIntegrador2\FinanceiroQuadraGo\DB_Config\FinanceiroQuadraGo.db')
cursor = conn.cursor()

# Define o período de interesse
start_date = datetime(2024, 7, 1)
end_date = datetime(2026, 12, 31)

# Função para adicionar meses
def add_months(start_date, months):
    return start_date + relativedelta(months=months)

# Loop para preencher a tabela PrevisaoLucro
current_date = start_date
while current_date <= end_date:
    # Calcula a receita estimada para o mês atual
    cursor.execute("""
        SELECT SUM(ValorReceita) AS TotalReceita
        FROM Receitas
        WHERE DATE(DataReceita) >= ? AND DATE(DataReceita) < ?
    """, (current_date.strftime('%Y-%m-01'), add_months(current_date, 1).strftime('%Y-%m-01')))

    result = cursor.fetchone()
    receita_estimativa = result[0] if result[0] is not None else 0.0

    # Calcula o custo estimado para o mês atual
    cursor.execute("""
        SELECT SUM(ValorCusto) AS TotalCusto
        FROM CustosOperacionais
        WHERE DATE(Data) >= ? AND DATE(Data) < ?
    """, (current_date.strftime('%Y-%m-01'), add_months(current_date, 1).strftime('%Y-%m-01')))

    result = cursor.fetchone()
    custo_estimativa = result[0] if result[0] is not None else 0.0

    # Arredonda os valores para 2 casas decimais
    receita_estimativa = round(receita_estimativa, 2)
    custo_estimativa = round(custo_estimativa, 2)

    # Calcula o lucro estimado
    lucro_estimado = round(receita_estimativa - custo_estimativa, 2)

    # Insere os dados na tabela PrevisaoLucro
    cursor.execute("""
        INSERT INTO PrevisaoLucro (Periodo, ReceitaEstimada, CustoEstimado, LucroEstimado)
        VALUES (?, ?, ?, ?)
    """, (current_date.strftime('%Y-%m'), receita_estimativa, custo_estimativa, lucro_estimado))

    # Avança para o próximo mês
    current_date = add_months(current_date, 1)

# Confirma as alterações e fecha a conexão
conn.commit()
conn.close()

print("Previsão de lucro preenchida com sucesso!")
