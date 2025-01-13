import pytest
import sqlite3
from app import app 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config["DATABASE"] = ':memory:' # Banco em memória para os testes

    # Criação do cliente de teste
    with app.test_client() as client:
        with app.app_context():
            # Inicializa o banco de dados antes de iniciar os testes
            init_db()
        yield client

def init_db():
    """Inicializa o banco de dados para os testes."""
    with sqlite3.connect(app.config["DATABASE"]) as con:
        cursor = con.cursor()
        # query que cria a tabela de usuarios
        query = '''CREATE TABLE IF NOT EXISTS "usuario" (
          "ID" INTEGER PRIMARY KEY AUTOINCREMENT, 
          "NOME" TEXT, 
          "IDADE" INTEGER, 
          "CIDADE" TEXT, 
          "ESTADO" TEXT, 
          "EMAIL" TEXT )
          '''

        # Executa o sql
        cursor.execute(query)
        con.commit()
