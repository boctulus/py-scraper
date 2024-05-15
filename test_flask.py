from flask import Flask, jsonify, request

app = Flask(__name__)

"""
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04#creating-the-wsgi-entry-point
"""

@app.route('/api/v1/scraper/robot/order', methods=['POST'])
def receive_order():
    # Obtener el JSON del body de la solicitud
    data = request.get_json()

    # Verificar si se proporcionó el campo "products" en el JSON
    if 'products' in data:
        products = data['products']
        # Aquí puedes procesar la lista de productos como necesites
        # Por ahora, simplemente devolveré la lista de productos recibida
        return jsonify({'products': products})
    else:
        # Si el campo "products" no está presente en el JSON, devuelve un error
        return jsonify({'error': 'Field "products" not found in JSON'}), 400

# Endpoint para obtener enlaces a todos los screenshots dado un order_id
@app.route('/api/v1/scraper/robot/screenshots/<order_id>', methods=['GET'])
def get_screenshots(order_id):
    # Aquí puedes obtener los enlaces a los screenshots para el order_id dado
    # Por ahora, devolveré un ejemplo de lista de enlaces
    screenshots = ['link1', 'link2', 'link3']  # Ejemplo de enlaces
    return jsonify({'screenshots': screenshots})

# Endpoint para obtener el último screenshot dado un order_id
@app.route('/api/v1/scraper/robot/screenshots/<order_id>/last', methods=['GET'])
def get_last_screenshot(order_id):
    # Aquí puedes obtener el último screenshot para el order_id dado
    last_screenshot = 'last_link'  # Ejemplo de enlace del último screenshot
    return jsonify({'last_screenshot': last_screenshot})

# Endpoint para obtener un screenshot específico dado un filename y order_id
@app.route('/api/v1/scraper/robot/screenshots/<order_id>', methods=['GET'])
def get_specific_screenshot(order_id):
    filename = request.args.get('filename')
    # Aquí puedes obtener el screenshot específico para el filename y order_id dado
    specific_screenshot = f'link_to_{filename}'  # Ejemplo de enlace al screenshot específico
    return jsonify({'specific_screenshot': specific_screenshot})

# Endpoint para obtener el estado del scraper
@app.route('/api/v1/scraper/robot/status', methods=['GET'])
def get_scraper_status():
    # Aquí puedes obtener y devolver el estado actual del scraper
    scraper_status = 'running'  # Ejemplo de estado del scraper
    return jsonify({'status': scraper_status})


"""
Para ejecutar en modo debug es con
    app.run(debug=True) 
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0') 
