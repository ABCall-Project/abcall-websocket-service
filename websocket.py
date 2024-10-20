from flask import Flask
from flask_socketio import SocketIO, emit
import json
import uuid
import re  # Importamos la librería de expresiones regulares
from flaskr.utils import helper

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
EMPTY_ERROR_RESPONSE = 'No entiendo tu solicitud, ¿podrías intentar nuevamente?'

waiting_for_description = False  # Si estamos esperando la descripción de un problema
waiting_for_email = False  # Si estamos esperando el correo electrónico
issue_description = None  # Descripción del problema
issue_created = False  # Si se ha creado la incidencia
user_email = None  # Correo electrónico del usuario

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def chatbot_response(message):
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
        return "Gracias. Por favor, proporciona tu correo electrónico para enviar la confirmación."
    elif waiting_for_email:
        if is_valid_email(message):
            user_email = message
            issue_id = uuid.uuid4().hex
            issue_created = True
            waiting_for_email = False  
            #TODO Aca llamar el Servicio
            return f"Hemos creado la incidencia: {issue_id}, y hemos enviado tu extracto al correo {user_email}.\nGracias por escribirnos.\n¿Algo más en lo que pueda colaborarte?"
        else:
            # Si el correo no es válido, pedimos nuevamente
            return "El formato del correo es inválido. Por favor, proporciona un correo válido."
    elif lower_cased_message == '3':
        return "Te estoy conectando con un agente..."
    elif 'no' in lower_cased_message and issue_created:
        return "Cerraremos la incidencia por el momento. ¡Gracias por comunicarte!"
    
    if helper.is_empty(message):
        return EMPTY_ERROR_RESPONSE

    return "No entiendo tu mensaje. ¿Puedes reformularlo?"


@app.route('/')
def index():
    return "El servidor WebSocket del chatbot está en funcionamiento"

@socketio.on('message')
def handle_message(message):
    data = json.loads(message)
    user_id = data.get('userId', 'unknown_user')
    user_message = data.get('message', '')
    print(f"Mensaje recibido del cliente: {user_message} y ID {user_id}")

    # Procesar el mensaje y generar una respuesta
    response = chatbot_response(message)
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9000, debug=True)
