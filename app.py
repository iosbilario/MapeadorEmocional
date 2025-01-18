from flask import Flask, render_template, request
import sqlite3
import requests

app = Flask(__name__)

def get_location_name(lat, lon):
    """Usa a API de geocodificação para obter a cidade e o país."""
    try:
        url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}'
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        city = data.get('address', {}).get('city', 'Desconhecido')
        country = data.get('address', {}).get('country', 'Desconhecido')
        return f"{city}, {country}"
    except Exception as e:
        return "Erro na API"

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, latitude, longitude FROM emotions")
    rows = cursor.fetchall()
    markers = [{'emotion': row[0], 'latitude': row[1], 'longitude': row[2]} for row in rows]
    conn.close()
    return render_template('index.html', markers=markers)


@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form['emotion']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    timestamp = request.form['timestamp']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emotions (emotion, latitude, longitude, timestamp) VALUES (?, ?, ?, ?)",
                   (emotion, latitude, longitude, timestamp))
    conn.commit()
    conn.close()

    return "<h1>Emoção registrada com sucesso!</h1><a href='/'>Voltar</a>"

@app.route('/emocoes')
def emocoes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, COUNT(*) as count FROM emotions GROUP BY emotion ORDER BY count DESC")
    records = cursor.fetchall()
    conn.close()

    return render_template('emocoes.html', records=records)

@app.route('/localidades')
def localidades():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT latitude, longitude FROM emotions")
    rows = cursor.fetchall()
    conn.close()

    location_counts = {}

    for lat, lon in rows:
        location = get_location_name(lat, lon)
        if location in location_counts:
            location_counts[location] += 1
        else:
            location_counts[location] = 1

    sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)

    return render_template('localidades.html', locations=sorted_locations)

if __name__ == '__main__':
    app.run(debug=True)
