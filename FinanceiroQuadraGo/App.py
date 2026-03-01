import sys
project_root = 'D:\\Bruno\\FATEC CDN\\ProjetoIntegrador2\\FinanceiroQuadraGo'
sys.path.append(project_root)

from flask import Flask
from Controllers.QuadrasController import quadrasController
from DB_Config.TabelasBancoDados import (
    init_db_custos_operacionais,
    init_db_esportes,
    init_db_previsao_lucro,
    init_db_produtos,
    init_db_proprietarios_quadra,
    init_db_quadra_esporte,
    init_db_quadras,
    init_db_receitas,
    init_db_reservas,
    init_db_usuarios,
    init_db_venda_produtos,
)

def inicializar_banco_tabelas():
    try:
        init_db_custos_operacionais()
        init_db_esportes()
        init_db_previsao_lucro()
        init_db_produtos()
        init_db_proprietarios_quadra()
        init_db_quadra_esporte()
        init_db_quadras()
        init_db_receitas()
        init_db_reservas()
        init_db_usuarios()
        init_db_venda_produtos()
        print("Todas as tabelas foram inicializadas com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao inicializar as tabelas: {e}")

app = Flask(__name__, template_folder="Templates")
app.register_blueprint(quadrasController, url_prefix='/')

if __name__ == "__main__":
    inicializar_banco_tabelas()
    app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=True)