#ChatBot inteligente con WhatsApp en Python
from flask import Flask, jsonify, request
import os
app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    #EXTRAEMOS EL TELEFONO DEL CLIENTE
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    #SI HAY UN MENSAJE
    if mensaje is not None:
      from rivescript import RiveScript
      bot = RiveScript()
      bot.load_file('example.rive')
      bot.sort_replies()
      #obtenemos respuesta
      respuesta= bot.reply("localuser",mensaje)
      respuesta=respuesta.replace("\\n","\\\n")
      respuesta=respuesta.replace("\\","")
      
      #dss
      f = open("texto.txt", "w")
      f.write(mensaje)
      f.close()
      #RETORNAMOS EL STATUS EN UN JSON
      enviar(telefonoCliente,respuesta)
      return jsonify({"status": "success"}, 200)


def enviar(telefonoRecibe,respuesta):
  from heyoo import WhatsApp
  #TOKEN DE ACCESO DE FACEBOOK
  token='EAAG5Yc1IB1oBAHywXDAzRgZAeWcGCcmeSmcZA4KaQuL7Qx1VaEDFWZCUnHrZCZBHdI9TiKp9ileS9KbZAP4pyYx2OYzmAOw8JgFsqiLsDsNwkSZCYuXPfRMI9r0oa2RUprV42NZCB1ZABs6Fe8Urmm0H95cZAuxrnEgjs1LfoNz5BmtdAeuadGnjOecy2ZBJz6ZBH1PJU99RVer2xgZDZD'
  #IDENTIFICADOR DE NÚMERO DE TELÉFONO
  idNumeroTeléfono='101723519584262'
  #INICIALIZAMOS ENVIO DE MENSAJES
  mensajeWa=WhatsApp(token,idNumeroTeléfono)
  telefonoRecibe=telefonoRecibe.replace("521","52")
  #ENVIAMOS UN MENSAJE DE TEXTO
  mensajeWa.send_message(respuesta,telefonoRecibe)

#INICIAMSO FLASK
if __name__ == "__main__":


  app.run(debug=True, port=os.getenv("PORT", default=5000))

