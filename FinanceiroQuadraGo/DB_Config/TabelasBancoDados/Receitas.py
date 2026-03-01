import json
import os
import sqlite3

def load_project_root():
    path = 'D:\\Bruno\\FATEC CDN\\ProjetoIntegrador2\\FinanceiroQuadraGo\\Config\\appSettings.json'
    with open(path, 'r') as file:
        config = json.load(file)
        return config.get('project_root', '')

project_root = load_project_root()
DB_PATH = os.path.join(project_root, 'DB_Config', 'FinanceiroQuadraGo.db')

def init_db_receitas():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Receitas (
            ID_Receita INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Origem INTEGER NOT NULL,
            Data_Receita DATE NOT NULL,
            Origem_Receita TEXT NOT NULL CHECK(Origem_Receita IN ('Reserva Quadra', 'Venda Produto')),
            Valor_Receita DECIMAL(10, 2) NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_receitas()