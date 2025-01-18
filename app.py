from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter marcadores do banco de dados
def get_markers():
    conn = get_db_connection()
    if not conn:
        return []  # Retorna uma lista vazia se houver falha no banco
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT emotion, latitude, longitude FROM emotions")
        rows = cursor.fetchall()
        return [{'emotion': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows]
    except sqlite3.Error as e:
        print(f"Erro ao obter marcadores: {e}")
        return []
    finally:
        conn.close()

# Rota principal
@app.route('/')
def index():
    markers = get_markers()
    return render_template('index.html', markers=markers)



@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form.get('emotion')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Gera o timestamp no formato correto

    # Validação de dados
    if not emotion or not latitude or not longitude:
        print(f"Dados recebidos: emotion={emotion}, latitude={latitude}, longitude={longitude}, timestamp={timestamp}")
        return f"""
        <h1>Dados inválidos. Certifique-se de preencher todos os campos.</h1>
        <p>Dados recebidos:</p>
        <ul>
            <li>Emotion: {emotion}</li>
            <li>Latitude: {latitude}</li>
            <li>Longitude: {longitude}</li>
            <li>Timestamp: {timestamp}</li>
        </ul>
        <a href='/'>Voltar</a>
        """, 400

    conn = get_db_connection()
    if not conn:
        return "<h1>Erro no servidor. Tente novamente mais tarde.</h1><a href='/'>Voltar</a>", 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emotions (emotion, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)",
            (emotion, latitude, longitude, timestamp)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir emoção: {e}")
        return "<h1>Erro ao salvar a emoção.</h1><a href='/'>Voltar</a>", 500
    finally:
        conn.close()

    return redirect(url_for('index'))

# Rota para visualizar emoções agregadas
@app.route('/emocoes')
def emocoes():
    conn = get_db_connection()
    if not conn:
        return "<h1>Erro no servidor. Tente novamente mais tarde.</h1><a href='/'>Voltar</a>", 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT emotion, COUNT(*) as count FROM emotions GROUP BY emotion ORDER BY count DESC")
        records = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao obter emoções: {e}")
        return "<h1>Erro ao carregar os registros.</h1><a href='/'>Voltar</a>", 500
    finally:
        conn.close()

    return render_template('emocoes.html', records=records)

if __name__ == '__main__':
    app.run(debug=bool(os.getenv('FLASK_DEBUG', True)))

