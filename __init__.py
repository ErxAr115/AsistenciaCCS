from flask import Flask, jsonify, request
from heyoo import WhatsApp
import mysql.connector
from rivescript import RiveScript
app = Flask(__name__)

customToken = 'AlphaOmega'
Token = 'EAAMEFRuQJEYBO5V68CbdLIexZCSsily5XAs8bgvtteJZBBy6Io6AgxvtFKYm1MuRw8O0rcXZAjacZBtOH6RYMPZB9ZBPIi2yvxxM7x9yugKkjvEfLOk6M2uZCcZBzCM09SFBxKvUMx3usDNtYkja4ciXPFENjRIU0G89B3r77bQCXqqzXc256CJlTQyr9I1hjVSi'
idNum = '163451000177784'

#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    if request.method == "GET":
        if request.args.get('hub.verify_token') == customToken:
            return request.args.get('hub.challenge')
        else:
          return "Error de autentificacion."
    data=request.get_json()
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    mensaje = acentos(mensaje)
    if mensaje is not None:
          bot = RiveScript()
          bot.load_file('chatbot.rive')
          bot.sort_replies()
          #OBTENEMOS LA RESPUESTA
          respuesta= bot.reply("localuser",mensaje)
          respuesta=respuesta.replace("\\n","\\\n")
          respuesta=respuesta.replace("\\","")
          #CONECTAMOS A LA BASE DE DATOS
          mydb = mysql.connector.connect(
          host = "mysql-ccschatbot.alwaysdata.net",
          user = "332032",
          password = "Lyla1295",
          database='ccschatbot_db'
          )
          mycursor = mydb.cursor()
          query="SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';"
          mycursor.execute("SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';")

          cantidad, = mycursor.fetchone()
          cantidad=str(cantidad)
          cantidad=int(cantidad)
          if cantidad==0 :
            sql = ("INSERT INTO registro"+ 
            "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
            "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoCliente+"');")
            mycursor.execute(sql)
            mydb.commit()
            enviar(telefonoCliente, respuesta)
            #RETORNAMOS EL STATUS EN UN JSON
            return jsonify({"status": "success"}, 200)
          mensaje = respuesta = ''
        
    
def enviar(telefonorecibe, respuesta):
   token = Token
   idNumeroTelefono = idNum
   mensaje = WhatsApp(token, idNumeroTelefono)
   telefonorecibe = telefonorecibe.replace("521", "52")
   mensaje.send_message(respuesta, telefonorecibe)

def acentos(mensaje):
   a,b = 'áéíóúü','aeiouu'
   trans = str.maketrans(a,b)
   nuevo = mensaje.translate(trans)
   return nuevo

#INICIAMSO FLASK
if __name__ == "__main__":
  app.run(debug=True)