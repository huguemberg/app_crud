from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from config import Config

# Cria uma instância da classe Flask
app = Flask(__name__)

# Busca a Secret Key do DB
app.config.from_object(Config)
app.config['DATABASE'] = ':memory:'

# Banco de dados SQLite
DATABASE = 'db_user.db'

#### ENDPOINTS ####


# Página inicial com as descrições dos endpoint.
@app.route('/')
def index():
    return render_template('formulario.html')


# 1. `GET /users`: Retorna a lista de todos os usuários.
@app.route("/users", methods=['GET'])
def get_usuarios():
    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario")
        dados = cursor.fetchall()
        return render_template("list_user.html", datas = dados)
    except sqlite3.Error as e:
        flash(f"Erro ao buscar dados: {str(e)}", "danger")
        return render_template("list_user.html", datas = [])
    finally:
        con.close()


# 2. `GET /users/{id}`: Retorna os detalhes de um usuário específico.
@app.route('/users/<int:id>', methods=["GET"])
def get_usuario(id):
    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id = ?", (id,))
        dado = cursor.fetchone()
        if dado:
            flash("Usuário encontrado.", "success")
            return render_template("list_user.html", datas = [dado])
        else:
            flash("Usuário não encontrado.", "warning")
            return redirect(url_for("get_usuarios"))
    except sqlite3.Error as e:
        flash(f"Erro ao buscar usuário: {str(e)}", "danger")
        return redirect(url_for("get_usuarios"))
    finally:
        con.close()


# 3. `POST /users`: Adiciona um novo usuário.
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            idade = request.form["idade"]
            cidade = request.form["cidade"]
            estado = request.form["estado"]
            email = request.form["email"]
            con = sqlite3.connect(DATABASE)
            cursor = con.cursor()
            cursor.execute("INSERT INTO usuario (NOME, IDADE, CIDADE, ESTADO, EMAIL) VALUES (?, ?, ?, ?, ?)",
                           (nome, idade, cidade, estado, email))
            con.commit()
            flash("Usuário cadastrado com sucesso.", "success")
            return redirect(url_for("get_usuarios"))
        except sqlite3.Error as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")
            return render_template("add_user.html")
        finally:
            con.close()
    return render_template("add_user.html")


# 4. `PUT /users/{id}`: Atualiza os dados de um usuário existente.
@app.route("/edit_user/<string:id>", methods=["POST", "GET"])
def edit_user(id):
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            idade = request.form["idade"]
            cidade = request.form["cidade"]
            estado = request.form["estado"]
            email = request.form["email"]
            con = sqlite3.connect(DATABASE)
            cursor = con.cursor()
            cursor.execute("UPDATE usuario SET NOME=?, IDADE=?, CIDADE=?, ESTADO=?, EMAIL=? WHERE id=?",
                           (nome, idade, cidade, estado, email, id))
            con.commit()
            flash("Dados atualizados com sucesso.", "success")
            return redirect(url_for("get_usuarios"))
        except sqlite3.Error as e:
            flash(f"Erro ao atualizar usuário: {str(e)}", "danger")
            return redirect(url_for("edit_user", id=id))
        finally:
            con.close()

    try:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id = ?", (id,))
        dado = cursor.fetchone()
        if dado:
            return render_template("edit_user.html", datas = dado)
        else:
            flash("Usuário não encontrado.", "warning")
            return redirect(url_for("get_usuarios"))
    except sqlite3.Error as e:
        flash(f"Erro ao carregar dados do usuário: {str(e)}", "danger")
        return redirect(url_for("get_usuarios"))
    finally:
        con.close()


# 5. `DELETE /users/{id}`: Remove um usuário.
@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    try:
        con = sqlite3.connect(DATABASE)
        cursor = con.cursor()
        cursor.execute("DELETE FROM usuario WHERE id=?", (id,))
        con.commit()
        flash("Usuário deletado com sucesso.", "warning")
    except sqlite3.Error as e:
        flash(f"Erro ao deletar usuário: {str(e)}", "danger")
    finally:
        con.close()
    return redirect(url_for("get_usuarios"))


if __name__ == '__main__':
    app.run()
