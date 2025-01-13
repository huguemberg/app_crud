import pytest
import sqlite3
from app import app


# 1 e 2. Testa se as rotas '/' e '/users' retornam 200

@pytest.mark.parametrize("route", [
    ('/'),
    ('/users'),
])
def test_routes(client, route):
    response = client.get(route)
    # Valida se a rota retorna 200
    assert response.status_code == 200



# 3. Testa um INSERT no banco de dados

@pytest.mark.parametrize("user_data", [
    {"nome": "Teste", "idade": 25, "cidade": "Cidade", "estado": "Estado", "email": "teste@teste.com"}
    ])

def test_insert_user(client, user_data):
    # Limpa a tabela antes do teste e inseri o user_data de teste
    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM usuario") 
        con.commit()

    response = client.post("/add_user", data = user_data)
    # Redireciona após inserção
    assert response.status_code == 302  

    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario")
        user = cursor.fetchone()

        # Valida se os dados foram inseridos corretamente
        assert user is not None
        assert user[1] == user_data['nome']
        assert isinstance(user[1], str)
        assert user[2] == user_data['idade']
        assert isinstance(user[2], int)
        assert user[3] == user_data['cidade']
        assert isinstance(user[3], str)
        assert user[4] == user_data['estado']
        assert isinstance(user[4], str)
        assert user[5] == user_data['email']
        assert isinstance(user[5], str)



# 4. Testa um UPDATE no banco de dados

def test_update_user(client):
    
    # Inseri um usuário para atualizar
    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO usuario (nome, idade, cidade, estado, email) VALUES (?, ?, ?, ?, ?)",
                       ("Teste", 25, "Cidade", "Estado", "teste@teste.com"))
        con.commit()
        user_id = cursor.lastrowid

    # Atualiza o usuário
    updated_data = {"nome": "Atualizado", "idade": 30, "cidade": "Nova Cidade", "estado": "Novo Estado", "email": "atualizado@teste.com"}
    response = client.post(f"/edit_user/{user_id}", data = updated_data)
    assert response.status_code == 302

    # Verifica se os dados foram atualizados
    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        assert user is not None
        assert user[1] == updated_data["nome"]
        assert user[2] == updated_data["idade"]
        assert user[3] == updated_data["cidade"]
        assert user[4] == updated_data["estado"]
        assert user[5] == updated_data["email"]


# 4. Testa um DELETE no banco de dados

def test_delete_user(client):
    # Inseri um usuário para deletar
    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO usuario (nome, idade, cidade, estado, email) VALUES (?, ?, ?, ?, ?)",
                       ("Teste", 25, "Cidade", "Estado", "teste@teste.com"))
        con.commit()
        user_id = cursor.lastrowid

    response = client.get(f"/delete_user/{user_id}")
    assert response.status_code == 302

    # Verifica se o usuário foi deletado
    with sqlite3.connect(app.config['DATABASE']) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        assert user is None