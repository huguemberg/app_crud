import sqlite3 as sql

# conectar ao banco de dados
con = sql.connect('db_user.db')
cursor = con.cursor()

# query que cria a tabela de usuarios
query = '''CREATE TABLE "usuario" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "IDADE" INTEGER,
    "CIDADE" TEXT,
    "ESTADO" TEXT,
    "EMAIL" TEXT
    )'''

# Executa o sql
cursor.execute(query)

# Commit das alterações
con.commit()

# Fechando a conexão
con.close()