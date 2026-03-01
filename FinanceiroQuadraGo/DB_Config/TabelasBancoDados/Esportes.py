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

def init_db_esportes():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Esportes (
            ID_Esporte INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Esporte VARCHAR(50) NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_esportes()