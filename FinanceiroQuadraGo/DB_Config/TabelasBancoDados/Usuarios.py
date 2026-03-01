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

def init_db_usuarios():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Usuario VARCHAR(100) NOT NULL,
            CPF VARCHAR(14) NOT NULL,
            Email VARCHAR(100),
            Telefone VARCHAR(20)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_usuarios()