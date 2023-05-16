#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import logging
import rasa.core.channels.channel
import requests
import sanic
import sanic.response


# In[ ]:

logger = logging.getLogger(__name__)
def _compose_tyntec_send_whatsapp_text_request(apikey, from_, to, text):
    return requests.Request(
        method="POST",
        url="https://waba-sandbox.360dialog.io/v1/messages",
        headers={
            "Accept": "application/json",
            "D360-API-KEY": apikey},
        json={
            "recipient_type": "individual",
            "to": to,
            "type":"text",
            "text": {
                "body": text}})


# In[ ]:


def _parse_tyntec_webhook_request(body):
    try:
        id_ = body["messages"][0]["id"]
        #print("----------id------------",id_)
        from_ = body["messages"][0]["from"]
        #print("----------from_------------",from_)
        channel = "whatsapp"
        content_type = body["messages"][0]["type"]
        #print("----------content_type------------",content_type)
        content_text = body["messages"][0]["text"]["body"]
        #print("----------content_text------------",content_text)
    except KeyError:
        raise ValueError("body not a tyntec WhatsApp text message event")
 
    if channel != "whatsapp" or content_type != "text":
        raise ValueError("body not a WhatsApp text message event")
 
    return _TyntecWhatsAppTextMessage(id_, from_, content_text)


# In[ ]:


class _TyntecWhatsAppTextMessage:
    def __init__(self, id_, from_, text):
        self.id = id_
        self.from_ = from_
        self.text = text


# In[ ]:


class TyntecInputChannel(rasa.core.channels.channel.InputChannel):
    def __init__(self, waba, tyntec_apikey, requests_session=None):
        if requests_session is None:
            requests_session = requests.Session()
 
        self.requests_session = requests_session
        self.tyntec_apikey = tyntec_apikey
        self.waba = waba
 
    @classmethod
    def from_credentials(cls, credentials):
        return cls(credentials["waba"], credentials["apikey"])
 
    @classmethod
    def name(cls):
        return "tyntec"
 
    def blueprint(self, on_new_message):
        custom_webhook = sanic.Blueprint("tyntec")
 
        @custom_webhook.route("/", methods=["GET"])
        async def health(request):
            return sanic.response.json({"status": "ok"})
 
        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request):
            try:
                text_message = _parse_tyntec_webhook_request(request.json)
                print("==============================================",request.json)
                #url_flask="http://127.0.0.1:5000/incomingmessage"
                #x = requests.post(url=url_flask, data = text_message)
                print("***************************text_message***************************",text_message)
            except ValueError:
                request_json = json.dumps(request.json)
                print("***************************EXCEPT*************************")
                logging.warning(f"Unsupported event skipped: {request_json}")
                return sanic.response.text(f"********Unsupported event skipped: {request_json}")
 
            await on_new_message(
                rasa.core.channels.channel.UserMessage(
                    text_message.text,
                    TyntecOutputChannel(self.waba, self.tyntec_apikey, self.requests_session),
                    text_message.from_,
                    input_channel=self.name(),
                    message_id=text_message.id))
 
            return sanic.response.text("OK")
        print("========================================================",custom_webhook)
        return custom_webhook
 
 
class TyntecOutputChannel(rasa.core.channels.channel.OutputChannel):
    def __init__(self, waba, tyntec_apikey, requests_session):
        self.requests_session = requests_session
        self.tyntec_apikey = tyntec_apikey
        self.waba = waba
 
    @classmethod
    def name(cls):
        return "tyntec"
 
    async def send_text_message(self, recipient_id, text, **kwargs):
        #API_ENDPOINT="https://waba-sandbox.360dialog.io/v1/messages"
        #logger.info("calling: " + API_ENDPOINT + " with text: " + text)
        #headers={
        #    "Accept": "application/json",
        #    "apikey": self.tyntec_apikey},
        #json_={
        #    "to": recipient_id,
        #    "type":"text",
        #   "text": {
        #        "body": text}}
        #requests.post(url=API_ENDPOINT, data=json.dumps(json_), headers=headers)
        #print("-----------------------------------text---------------------------------",text)
        request = _compose_tyntec_send_whatsapp_text_request(self.tyntec_apikey, self.waba, recipient_id, text)
        print("==================================================Request===================================",recipient_id)
        prepared_request = request.prepare()
 
        response = self.requests_session.send(prepared_request)
        response.raise_for_status()

        
