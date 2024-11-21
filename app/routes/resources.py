import requests
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

resources_bp = Blueprint("resources", __name__)

@resources_bp.route("/", methods=["GET"])
@jwt_required()

def get_external_resources():
    # URL y token de la API externa
    EXTERNAL_API_URL = "http://consultas.cuc.edu.co/api/v1.0/recursos"
    EXTERNAL_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6InBydWViYTIwMjJAY3VjLmVkdS5jbyIsImV4cCI6MTY0OTQ1MzA1NCwiY29ycmVvIjoicHJ1ZWJhMjAyMkBjdWMuZWR1LmNvIn0.MAoFJE2SBgHvp9BS9fyBmb2gZzD0BHGPiyKoAo_uYAQ"

    # Encabezados para la solicitud
    headers = {
        "Authorization": f"JWT {EXTERNAL_API_TOKEN}"
    }

    try:
        # Hacer la solicitud a la API externa
        response = requests.get(EXTERNAL_API_URL, headers=headers)
        response.raise_for_status()  # Lanza un error si la solicitud falla

        print(response)
        # Retornar la respuesta al cliente
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        # Manejar errores de la solicitud externa
        return jsonify({"error": "No se pudieron obtener los recursos externos", "details": str(e)}), 500
    
    
