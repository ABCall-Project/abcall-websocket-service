from flask import Flask
from flask_socketio import SocketIO, emit
import json
import uuid
import re  # Importamos la librería de expresiones regulares
from flaskr.utils import helper
import requests
from  config import Config

config = Config()
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
EMPTY_ERROR_RESPONSE = 'No entiendo tu solicitud, ¿podrías intentar nuevamente?'
AUTH_USER_AGENT_ID = '5541639d-2509-4a5d-9877-588d351bb92f'
HOST = config.URL_ISSUES_SERVICE

waiting_for_description = False  # Si estamos esperando la descripción de un problema
waiting_for_email = False  # Si estamos esperando el correo electrónico
issue_description = None  # Descripción del problema
issue_created = False  # Si se ha creado la incidencia
user_email = None  # Correo electrónico del usuario

def chatbot_response(message,user_id):
    
    global waiting_for_description, waiting_for_email, issue_description, issue_created, user_email

    lower_cased_message = message.strip().lower()

    if 'error' in lower_cased_message:
        return "Parece que estás enfrentando un error. ¿Puedes darme más detalles?"
    elif 'hola' in lower_cased_message:
        return "¡Hola! ¿En qué puedo ayudarte hoy?"
    elif 'opciones' in lower_cased_message or 'ayuda' in lower_cased_message:
        return "Aquí tienes algunas opciones:\n1. Consultar tu saldo\n2. Reportar un problema\n3. Hablar con un agente"
    elif lower_cased_message == '1':
        return "Tu saldo actual es de $1000."
    elif lower_cased_message == '2' or 'incidente' in lower_cased_message:
        if not waiting_for_description:
            waiting_for_description = True
            return "Por favor, describe el problema que estás experimentando para que podamos crear una incidencia."
    elif waiting_for_description:
        issue_description = message
        waiting_for_description = False
        waiting_for_email = True  
        payload = {
            "auth_user_id": user_id,
            "auth_user_agent_id": AUTH_USER_AGENT_ID,
            "subject": 'Incidente por chatbot',
            "description": issue_description
            }
        try:
            response = requests.post(f"{HOST}/issue/post", json=payload)
            response.raise_for_status() 
            return f"Hemos creado la incidencia.\nGracias por escribirnos.\n¿Algo más en lo que pueda colaborarte?"
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el Issue: {e}")
            return f"Hubo un error al crear la incidencia:"

    elif lower_cased_message == '3':
        return "Te estoy conectando con un agente..."
    elif 'no' in lower_cased_message or issue_created:
        return "Cerraremos la incidencia por el momento. ¡Gracias por comunicarte!"

    return EMPTY_ERROR_RESPONSE


@app.route('/')
def index():
    return "Chatbot WebSocket server is running"

@socketio.on('message')
def handle_message(message):
    data = json.loads(message)
    user_id = data.get('userId')
    user_message = data.get('message')

    # Procesar el mensaje y generar una respuesta
    response = chatbot_response(user_message,user_id)
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000, debug=True)
