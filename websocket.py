from flask import Flask
from flask_socketio import SocketIO, emit
import random
from flaskr.utils import helper

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
EMPTY_ERROR_RESPONSE = 'No entiendo tu solicitud, ¿podrías intentar nuevamente?'

def chatbot_response(message):
    responses = [
        "Hello! How can I assist you?",
        "I'm here to help!",
        "Feel free to ask me anything.",
        "I am a chatbot, how can I assist you today?"
    ]

    if helper.is_empty(message):
        return EMPTY_ERROR_RESPONSE
        

    return random.choice(responses)

@app.route('/')
def index():
    return "Chatbot WebSocket server is running"

@socketio.on('message')
def handle_message(message):
    print(f"Received message from client: {message}")

    response = chatbot_response(message)
    emit('response', response)

if __name__ == '__main__':
    # Run the WebSocket server
    socketio.run(app, host='0.0.0.0', port=9000, debug=True)