from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

datos = pd.read_csv('Vacunacion_Data.csv')

# Imprime los nombres de las columnas
print(datos.columns)

@app.route('/vacunacion/<int:anio>')
def obtener_vacunacion_por_anio(anio):
    columna_anio = f'{anio} [YR{anio}]'
    vacunacion = datos.loc[datos[columna_anio].notnull(), columna_anio].values
    if vacunacion.size > 0:
        return jsonify({'anio': anio, 'vacunacion': vacunacion[0]})
    else:
        return jsonify({'error': 'Año no encontrado'}), 404

@app.route('/vacunacion')
def obtener_vacunacion():
    columnas_anios = [col for col in datos.columns if col.startswith('1') or col.startswith('2')]
    vacunacion = datos[columnas_anios].melt(var_name='Anio', value_name='Vacunacion').dropna().to_dict(orient='records')
    return jsonify(vacunacion)

if __name__ == '__main__':
    app.run(debug=True)