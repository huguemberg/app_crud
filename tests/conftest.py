import pytest
import sqlite3
from app import app 

# Defini o cliente e a configuração de um banco de teste
@pytest.fixture
def client(tmp_path):
    # Caminho para o banco temporário
    temp_db = tmp_path / 'test_db_user.db'
    app.config['TESTING'] = True
    app.config['DATABASE'] = str(temp_db)

    # Criação do cliente de teste
    with app.test_client() as client:
        with app.app_context():
            # Inicializa o banco de dados
            init_db(app.config['DATABASE'])
        yield client

    # Fecha qualquer conexão pendente
    sqlite3.connect(app.config['DATABASE']).close()

def init_db(db_path):
    # Inicializa o banco de dados para os testes
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        # query que cria a tabela de usuarios
        query = '''CREATE TABLE IF NOT EXISTS "usuario" (
                "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
                "NOME" TEXT,
                "IDADE" INTEGER,
                "CIDADE" TEXT,
                "ESTADO" TEXT,
                "EMAIL" TEXT
                )
                '''

        # Executa o sql
        cursor.execute(query)
        con.commit()
