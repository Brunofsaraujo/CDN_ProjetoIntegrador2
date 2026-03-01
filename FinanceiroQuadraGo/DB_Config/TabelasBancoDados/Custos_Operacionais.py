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

def init_db_custos_operacionais():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Custos_Operacionais (
            ID_Custo INTEGER PRIMARY KEY AUTOINCREMENT,
            Descricao VARCHAR(255) NOT NULL,
            Valor_Custo DECIMAL(10, 2) NOT NULL,
            Tipo_Custo NVARCHAR(20) NOT NULL CHECK(Tipo_Custo IN ('Recorrente', 'Não Recorrente')),
            Categoria VARCHAR(50) NOT NULL,
            Data DATE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_custos_operacionais()