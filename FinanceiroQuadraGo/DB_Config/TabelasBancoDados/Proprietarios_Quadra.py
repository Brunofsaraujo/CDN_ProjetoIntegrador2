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

def init_db_proprietarios_quadra():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Proprietarios_Quadra (
            ID_Proprietario_Quadra INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Proprietario VARCHAR(100) NOT NULL,
            CPF_CNPJ VARCHAR(20) NOT NULL,
            Contato VARCHAR(50)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_proprietarios_quadra()