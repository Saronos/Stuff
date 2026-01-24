from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Leemos una variable de entorno para simular cambios de configuración
    modo = os.getenv('MODO_OPERATIVO', 'NORMAL')
    return jsonify({"message": "Hola Taylinn v1", "mode": modo, "status": "OK"})

@app.route('/health')
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
