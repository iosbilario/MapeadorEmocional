from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Garantir que markers seja sempre inicializado como uma lista vazia
    return render_template('index.html', markers=[])

@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form['emotion']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emotions (emotion, latitude, longitude) VALUES (?, ?, ?)', 
                   (emotion, latitude, longitude))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/emocoes')
def emocoes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT emotion, latitude, longitude FROM emotions')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return '<h1>Nenhuma emoção foi registrada ainda.</h1><a href="/">Voltar para o início</a>'
    
    formatted_emotions = ''.join([f'<li>{emotion} em [{latitude}, {longitude}]</li>' for emotion, latitude, longitude in rows])
    return f'''
        <h1>Emoções Coletadas</h1>
        <ul>
            {formatted_emotions}
        </ul>
        <a href="/">Voltar para o início</a>
    '''

@app.route('/mapa')
def mapa():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT emotion, latitude, longitude FROM emotions')
    rows = cursor.fetchall()
    conn.close()
    
    markers = [{'emotion': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows]
    return render_template('index.html', markers=markers)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
