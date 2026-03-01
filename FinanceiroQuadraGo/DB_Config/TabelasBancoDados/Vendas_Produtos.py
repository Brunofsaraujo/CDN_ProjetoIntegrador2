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

def init_db_venda_produtos():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vendas_Produtos (
            ID_Venda_Produtos INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Usuario INTEGER,
            ID_Produto INTEGER,
            Quantidade INTEGER NOT NULL,
            Valor_Total DECIMAL(10, 2) NOT NULL,
            Data_Venda DATE NOT NULL,
            FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
            FOREIGN KEY (ID_Produto) REFERENCES Produtos(ID_Produto)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_venda_produtos()