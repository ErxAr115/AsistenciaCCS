from flask import Blueprint, request
import sett, services

chat = Blueprint('chat', __name__)

@chat.route('/')
def home():
    return 'Hello World!'

@chat.route('/webhook')
def checkToken():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == sett.token and challenge != None:
            return challenge
        else:
            return 'Error. Token incorrecto.', 403
    except Exception as E:
        return E, 403
    
@chat.route('/webhook', methods=['POST'])
def receiveMessage():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.getWhatsappMessage(message)
        services.adminChatbot(text, number, messageId, name)

        return 'enviado'
    except Exception as E:
        return E, 403