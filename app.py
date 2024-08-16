from flask import Flask, request, jsonify, render_template
import locale

app = Flask(__name__)

# Configurar locale para el formato de números
locale.setlocale(locale.LC_ALL, 'es_PE.UTF-8')  # Ajusta el locale según tu región

class EmpresaManager:
    def __init__(self):
        self._database = {}

    def agregar_empresa(self, nombre, direccion, telefono, cantidad_trabajadores, pago_trabajadores):
        # Calcular el presupuesto mensual
        presupuesto = cantidad_trabajadores * pago_trabajadores * 30
        
        # Formatear el presupuesto
        presupuesto_formateado = locale.format_string('%.2f', presupuesto, grouping=True)
        
        # Guardar en la base de datos simulada
        self._database[nombre] = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'cantidad_trabajadores': cantidad_trabajadores,
            'pago_trabajadores': pago_trabajadores,
            'presupuesto': presupuesto_formateado
        }
        return {"message": "Datos guardados correctamente"}

    def buscar_empresa(self, nombre):
        return self._database.get(nombre, None)

# Instancia del manejador de empresas
empresa_manager = EmpresaManager()

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para recibir datos de la empresa
@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    nombre = data['nombre']
    direccion = data['direccion']
    telefono = data['telefono']
    cantidad_trabajadores = int(data['cantidad_trabajadores'])
    pago_trabajadores = float(data['pago_trabajadores'])
    
    result = empresa_manager.agregar_empresa(
        nombre, direccion, telefono, cantidad_trabajadores, pago_trabajadores
    )
    
    return jsonify(result), 200

# Ruta para buscar una empresa por nombre
@app.route('/buscar', methods=['GET'])
def buscar_empresa():
    nombre = request.args.get('nombre')
    data = empresa_manager.buscar_empresa(nombre)
    
    if data:
        return render_template('result.html', data=data)
    else:
        return jsonify({"error": "Empresa no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
