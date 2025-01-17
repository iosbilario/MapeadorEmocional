from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para obter marcadores do banco de dados
def get_markers():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, latitude, longitude FROM emotions")
    rows = cursor.fetchall()
    conn.close()
    return [{'emotion': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows]

# Rota principal
@app.route('/')
def index():
    markers = get_markers()
    return render_template('index.html', markers=markers)

# Rota do mapa
@app.route('/mapa')
def mapa():
    markers = get_markers()
    return render_template('mapa.html', markers=markers)

# Rota para salvar emoções
@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form['emotion']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emotions (emotion, latitude, longitude) VALUES (?, ?, ?)",
                   (emotion, latitude, longitude))
    conn.commit()
    conn.close()

    return redirect('/')

# Rota para listar todas as emoções
@app.route('/emocoes')
def emocoes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, latitude, longitude FROM emotions")
    rows = cursor.fetchall()
    conn.close()
    return render_template('emocoes.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
