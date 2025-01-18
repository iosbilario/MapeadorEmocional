import sqlite3

# Conectar ao banco (será criado se não existir)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar a tabela 'emotions' com a coluna `timestamp`
cursor.execute("""
CREATE TABLE IF NOT EXISTS emotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    timestamp TEXT DEFAULT (datetime('now'))
)
""")

# Salvar mudanças e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados configurado com sucesso!")


