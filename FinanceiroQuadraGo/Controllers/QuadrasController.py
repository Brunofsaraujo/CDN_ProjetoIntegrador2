import json
import os
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

def load_project_root():
    path = 'D:\\Bruno\\FATEC CDN\\ProjetoIntegrador2\\FinanceiroQuadraGo\\Config\\appSettings.json'
    with open(path, 'r') as file:
        config = json.load(file)
        return config.get('project_root', '')

project_root = load_project_root()
DB_PATH = os.path.join(project_root, 'DB_Config', 'FinanceiroQuadraGo.db')

quadrasController = Blueprint('quadras', __name__)

def get_db_connection():
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@quadrasController.route('/teste')
def test():
    return str(DB_PATH)

@quadrasController.route('/')
def index():    
    conn = get_db_connection()
    quadras = conn.execute('SELECT * FROM Quadras').fetchall()
    conn.close()
    return render_template('index.html', quadras=quadras)

@quadrasController.route('/add', methods=('GET', 'POST'))
def add_quadra():
    if request.method == 'POST':
        nomeQuadra = request.form['Nome_Quadra']
        localizacao = request.form['Localizacao']
        preco_Hora = request.form['Preco_Hora']
        ativo = request.form['Ativo']

        conn = None
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO Quadras (Nome_Quadra, Localizacao, Preco_Hora, Ativo) VALUES (?, ?, ?, ?)',
                         (nomeQuadra, localizacao, preco_Hora, ativo))
            conn.commit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
        
        return redirect(url_for('quadras.index'))
    
    return render_template('addQuadra.html')

@quadrasController.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_quadra(id):
    if request.method == 'POST':
        nome_quadra = request.form.get('Nome_Quadra')
        localizacao = request.form.get('Localizacao')
        preco_hora = request.form.get('Preco_Hora')
        ativo = request.form.get('Ativo', 'N')

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Quadras
                SET Nome_Quadra = ?, Localizacao = ?, Preco_Hora = ?, Ativo = ?
                WHERE ID_Quadra = ?
            ''', (nome_quadra, localizacao, preco_hora, ativo, id))
            conn.commit()
        except Exception as e:
            print(f"Ocorreu um erro ao editar a quadra: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
        
        return redirect(url_for('quadras.index'))

    conn = None
    quadra = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        quadras = cursor.execute('SELECT * FROM Quadras WHERE ID_Quadra = ?', (id,)).fetchone()
    except Exception as e:
        print(f"Ocorreu um erro ao buscar a quadra: {e}")
    finally:
        if conn:
            conn.close()

    return render_template('editQuadra.html', quadra=quadras)

@quadrasController.route('/delete/<int:id>', methods=('POST',))
def delete_quadra(id):
    conn = None
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM Quadras WHERE ID_Quadra = ?', (id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao deletar a quadra: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return redirect(url_for('quadras.index'))