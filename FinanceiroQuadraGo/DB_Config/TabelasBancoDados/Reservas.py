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

def init_db_reservas():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reservas (
            ID_Reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Quadra INTEGER,
            ID_Usuario INTEGER,
            ID_Esporte INTEGER,
            Data_Reserva DATE NOT NULL,
            Hora_Inicio TIME NOT NULL,
            Hora_Fim TIME NOT NULL,
            Valor_Total DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (ID_Quadra) REFERENCES Quadras(ID_Quadra),
            FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),
            FOREIGN KEY (ID_Esporte) REFERENCES Esportes(ID_Esporte)
        )
    ''')
    
    conn.commit()
    conn.close()

init_db_reservas()