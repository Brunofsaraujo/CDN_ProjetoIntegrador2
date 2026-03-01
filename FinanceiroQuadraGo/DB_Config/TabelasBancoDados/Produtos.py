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

def init_db_produtos():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            ID_Produto INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome_Produto VARCHAR(100) NOT NULL,
            Preco_Unitario DECIMAL(10, 2) NOT NULL,
            Categoria VARCHAR(50)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_produtos()