from flask import Flask, render_template, request
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
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h1>Mapeador Emocional</h1>
        <form method="POST" action="/submit">
            <label for="emotion">Como você está se sentindo?</label>
            <input type="text" id="emotion" name="emotion" required>
            <br>
            <label for="location">Sua localização:</label>
            <input type="text" id="location" name="location" required>
            <button type="submit">Enviar</button>
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form['emotion']
    location = request.form['location']
    
    # Inserir dados no banco
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emotions (emotion, location) VALUES (?, ?)', (emotion, location))
    conn.commit()
    conn.close()
    
    return f'<h1>Obrigado por compartilhar: {emotion} de {location}</h1>'

@app.route('/emocoes')
def emocoes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT emotion, location FROM emotions')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return '<h1>Nenhuma emoção foi registrada ainda.</h1><a href="/">Voltar para o início</a>'
    
    formatted_emotions = ''.join([f'<li>{emotion} de {location}</li>' for emotion, location in rows])
    return f'''
        <h1>Emoções Coletadas</h1>
        <ul>
            {formatted_emotions}
        </ul>
        <a href="/">Voltar para o início</a>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
