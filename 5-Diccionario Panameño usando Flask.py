from flask import Flask, request, render_template, redirect, url_for
import redis

app = Flask(__name__)

redis_url = "redis://default:LApzhSSk8YSwXIshipytd2PIEQutVyv5@redis-18733.c228.us-central1-1.gce.cloud.redislabs.com:18733"
r = redis.from_url(redis_url)

@app.route('/')
def index():
    palabras = r.keys()
    palabras_significados = [(palabra.decode('utf-8'), r.get(palabra).decode('utf-8')) for palabra in palabras]
    return render_template('index.html', palabras_significados=palabras_significados)

@app.route('/agregar', methods=['POST'])
def agregar_palabra():
    palabra = request.form['palabra']
    significado = request.form['significado']
    r.set(palabra, significado)
    return redirect(url_for('index'))

@app.route('/editar', methods=['POST'])
def editar_palabra():
    palabra = request.form['palabra']
    nuevo_significado = request.form['nuevo_significado']
    if r.exists(palabra):
        r.set(palabra, nuevo_significado)
    return redirect(url_for('index'))

@app.route('/eliminar', methods=['POST'])
def eliminar_palabra():
    palabra = request.form['palabra']
    if r.exists(palabra):
        r.delete(palabra)
    return redirect(url_for('index'))

@app.route('/buscar', methods=['POST'])
def buscar_palabra():
    palabra = request.form['palabra']
    resultado = r.get(palabra)
    if resultado:
        return palabra + ": " + resultado.decode('utf-8')
    else:
        return "Palabra no encontrada."

if __name__ == '__main__':
    app.run(debug=True)