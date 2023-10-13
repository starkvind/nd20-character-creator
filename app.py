from flask import Flask, render_template, request, jsonify
from create_char import create_character  # Importa tus funciones de generación de personajes

app = Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/generar_personaje', methods=['POST'])
def generar_personaje():
    # Obtén el nivel del formulario (si se proporciona)
    nivel = request.form.get('nivel')
    opciones = request.form.get('opciones')
    if nivel is not None and nivel.isdigit():
        nivel = int(nivel)
    else:
        nivel = 1
    #print("Generando un personaje de nivel ", nivel)
    # Llama a tus funciones de generación de personajes aquí
    # Pasa el nivel como argumento
    resultado = create_character(nivel, False, opciones)
    
    # Devuelve el resultado en formato JSON incluyendo el personaje y el texto generado
    response = {
        "personaje": resultado
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    

