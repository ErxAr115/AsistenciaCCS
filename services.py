import requests, sett, json, messages

def getWhatsappMessage(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    return text

def sendWhatsappMessage(data):
    try:
        token = sett.whatsapp_token
        url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json', 
                   'Authorization': 'Bearer ' + token}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return 'Mensaje Enviado', 200
        else:
            return 'Error al enviar el mensaje', response.status_code
    except Exception as E:
        return E, 403
    
def textMessage(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def listReplyMessage(number, options, body, footer, sedd, messageID):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )
    
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def adminChatbot(text, number, messageId, name):
    text = text.lower()
    list = []

    if 'hola' in text:
        body = "¡Hola! Gracias por utilizar nuestro servicio de asistencia virtual. A continuación, le mostramos los servicios que ofrecemos:"
        footer = "Asistencia CCS"
        options = ["Información General", "Cursos de verano", "Grupos escolares", "Visitas", "Finalizar"]
        listData = listReplyMessage(number, options, body, footer, "sed2", messageId)
        list.append(listData)
    elif 'información general' in text:
        body = "Información general para público general"
        footer = "Asistencia CCS"
        options = ["Tarifas", "Horarios de atención", "Medios de contacto", "Regresar"]
        listData = listReplyMessage(number, options, body, footer, "sed2", messageId)
        list.append(listData)
    elif 'tarifas' in text:
        data = textMessage(number, messages.tarifas)
        list.append(data)
    elif 'horarios de atención' in text:
        data = textMessage(number, messages.horarios)
        list.append(data)
    else:
        data = textMessage(number, 'Lo siento. No comprendí tu mensaje.')
        list.append(data)

    for item in list:
        sendWhatsappMessage(item)