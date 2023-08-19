from flask import Flask, request, render_template, redirect, url_for
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    palabras = [(palabra.decode('utf-8'), r.get(palabra).decode('utf-8')) for palabra in r.keys()]
    return render_template('index.html', palabras=palabras)

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
    r.set(palabra, nuevo_significado)
    return redirect(url_for('index'))

@app.route('/eliminar', methods=['POST'])
def eliminar_palabra():
    palabra = request.form['palabra']
    r.delete(palabra)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)