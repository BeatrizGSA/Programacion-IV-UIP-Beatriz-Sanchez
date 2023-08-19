from flask import Flask, request, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    palabras = [(palabra.decode('utf-8'), r.get(palabra).decode('utf-8')) for palabra in r.keys()]
    # Construye el HTML directamente en lugar de utilizar una plantilla
    html = "<h1>Diccionario de Slang Panameño</h1>"
    # Agrega el resto del HTML aquí
    return html

@app.route('/agregar', methods=['POST'])
def agregar_palabra():
    palabra = request.form['palabra']
    significado = request.form['significado']
    r.set(palabra, significado)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)