from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Mapeador Emocional</h1>
        <form method="POST" action="/submit">
            <label for="emotion">Como você está se sentindo?</label>
            <input type="text" id="emotion" name="emotion" required>
            <button type="submit">Enviar</button>
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    emotion = request.form['emotion']
    # Salvar a emoção em um arquivo
    with open('emotions.txt', 'a') as f:
        f.write(emotion + '\n')
    return f'<h1>Obrigado por compartilhar: {emotion}</h1>'

@app.route('/emocoes')
def emocoes():
    try:
        with open('emotions.txt', 'r') as f:
            emotions = f.readlines()
        # Transformar as emoções em uma lista formatada
        formatted_emotions = ''.join([f'<li>{emotion.strip()}</li>' for emotion in emotions])
        return f'''
            <h1>Emoções Coletadas</h1>
            <ul>
                {formatted_emotions}
            </ul>
            <a href="/">Voltar para o início</a>
        '''
    except FileNotFoundError:
        return '<h1>Nenhuma emoção foi registrada ainda.</h1><a href="/">Voltar para o início</a>'

if __name__ == '__main__':
    app.run(debug=True)
