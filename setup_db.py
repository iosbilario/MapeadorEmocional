import sqlite3

# Conectar ao banco de dados (será criado automaticamente se não existir)
conn = sqlite3.connect('database.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Criar a tabela 'emotions' caso ainda não exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
)
''')

# Salvar mudanças e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados configurado com sucesso!")
