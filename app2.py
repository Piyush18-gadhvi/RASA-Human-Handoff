import json
from flask import Flask, request, render_template, Response
import requests
import json
import logging
import rasa.core.channels.channel
import requests
import sanic
import sanic.response
import queue
from rasa_sdk import Action, Tracker

# standard Python
#from addons.customChannelConnector import TyntecInputChannel, TyntecOutputChannel, _TyntecWhatsAppTextMessage

app = Flask(__name__, template_folder='template')
#socketio = SocketIO(app)
apikey= "grvAgQ_sandbox"
### GET Request to check the server is up and running ######
@app.route('/', methods = ['GET'])
def index():
    return render_template('display_message.html')


### RASA and Flask API integration ###

@app.route('/submit_text',methods = ['POST','GET'])
def submit_text():
    print("-----------------------Here---------------------")
    val = str(request.args.get('text'))
    print("---------------------------val------------------------",val)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {"sender": "Rasa", "message": val}
    res = requests.post(' https://7eea-223-236-119-236.ngrok.io/webhooks/rest/webhook', data=json.dumps(data), headers=headers)
    res = res.json()
    print("-------------------------------------------------------",res)
    val = res[0]['text']
    return "Bye" #render_template('index.html', val=val)

### Webhook set to Recieve the message from whatsapp tp flask API ###

class Database:
    def __init__(self):
        self.message_queue=queue.Queue(maxsize=100)
        self.human_handoff=False
        #self.message=message
    #def update():
    #    self.message_list.append(self.message)

db=Database()
#for i in range(0,40):
    #db.message_queue.put(i)

@app.route('/webhook/wamessages', methods= ['POST', 'GET'])
def wamessages():
    if request.method=="POST":
        data = request.json
        try:
            data["messages"][0]["text"]["body"]
            print("----------------------DATA-------------------",data)
            mes=data["messages"][0]["text"]["body"]
            if mes=="Human handoff":
                db.human_handoff=True
            if db.human_handoff:
                try:
                    db.message_queue.put(mes)
                    print("============Here=========")
                    #print("***************************text_message***************************",text_message)
                except ValueError :
                    request_json = json.dumps(request.json)
                    print("***************************EXCEPT*************************")
            print("----------human hand off",db.human_handoff)
            if not db.human_handoff:
                #print("-----------------------Here---------------------")
                #print("---------------------------mes------------------------",mes)
                headers_rasa = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                data = {"sender": "YourName", "message": mes}
                res = requests.post(' https://7eea-223-236-119-236.ngrok.io/webhooks/rest/webhook', data=json.dumps(data), headers=headers_rasa)
                res = res.json()
                print("-------------------------------------------------------",res)
                #print("***************************************ID*************************",(tracker.sender_id))
                val = res[0]['text']
                #print("---------------------------val------------------------",val)
                url_message="https://waba-sandbox.360dialog.io/v1/messages"
                headers_wa = {"D360-API-KEY":"grvAgQ_sandbox", 'content-type': 'application/json'}
                body_message={
                    "to": "YourNumber",
                    "type": "text",
                    "text": {
                        "body": val
                    }
                }
                mess_send=_compose_and_send_whatsapp_text_request(apikey, 'RASA','YourNumber', val)
                #print(mess_send)
            return "Yay"
        except KeyError :
            request_json = json.dumps(request.json)
            return "Please ignore the message"
        
@app.route('/display_message', methods=['GET'])
def display_message():
    print("1")
    if not db.message_queue.empty():
        message=db.message_queue.get_nowait()
        print("********************MESSAGE***********************",message)
    else:
        message=""
    return {"message":str(message)}

@app.route('/send_data', methods=['POST'])
def send_data():
    message=request.form['data']
    if str(message)=="unpause":
        send_req=_compose_and_send_whatsapp_text_request(apikey, "Agent", "YourNumber", "Thanks for talking to the live agent. Please type Hi to continue")
        #headers_rasa = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #data = {"sender": "YourName", "message": "/restart"}
        #res = requests.post('https://a559-115-119-250-30.ngrok.io/webhooks/rest/webhook', data=json.dumps(data), headers=headers_rasa)
        print("******************************This is unpause**************************")
        db.human_handoff=False
    if str(message) != "unpause":
        print("*********************************Form Data*******************", message)
        send_req=_compose_and_send_whatsapp_text_request(apikey, "Agent", "YourNumber", str(message))
    return {"message":str(message)}

def _parse_tyntec_webhook_request(body):   ### Function to parse the whatsapp message recieved
    try:
        id_ = body["messages"][0]["id"]
        from_ = body["messages"][0]["from"]
        channel = "whatsapp"
        content_type = body["messages"][0]["type"]
        content_text = body["messages"][0]["text"]["body"]
    except KeyError:
        raise ValueError("There is a key error")
 
    if channel != "whatsapp" or content_type != "text":
        raise ValueError("Not a proper message")
 
    return {"sender_id":id_,"from": from_, "text_message":content_text}        

def _compose_and_send_whatsapp_text_request(apikey, from_, to, text):
    url_message="https://waba-sandbox.360dialog.io/v1/messages"
    headers_wa = {"D360-API-KEY":"grvAgQ_sandbox", 'content-type': 'application/json'}
    body_message={"to": "YourNumber","type": "text","text": {"body": text}}
    x1=requests.post(url=url_message,data=json.dumps(body_message), headers = headers_wa)
    return x1.status_code

if __name__ == '__main__':
    app.run(port=8080,debug=True)
