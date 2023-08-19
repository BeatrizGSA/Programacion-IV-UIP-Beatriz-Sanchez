from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('datosrelacionadaconvacunacióncontraelsarampiónenniñosentre12-23mesesenPanamá.csv')

@app.route('/vacunacion/<int:anio>')
def obtener_vacunacion_por_anio(anio):
    vacunacion = data.loc[data['Year'] == anio, 'Value'].values
    if vacunacion.size > 0:
        return jsonify({'anio': anio, 'vacunacion': vacunacion[0]})
    else:
        return jsonify({'error': 'Año no encontrado'}), 404

@app.route('/vacunacion')
def obtener_vacunacion():
    vacunacion = data[['Year', 'Value']].to_dict(orient='records')
    return jsonify(vacunacion)

if __name__ == '__main__':
    app.run(debug=True)