# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# WATI, 360dialogue, chattigo, Freshdesk,infobip, sprinklr 
# I would like to know about the services provided by your platform and would also like to discuss the possibility of integrating my custom middleware with your service which will respond to customer queries accordingly in appropriate manner. 

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_core_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher
from rasa_core_sdk.events import (ConversationPaused, UserUtteranceReverted, ConversationResumed, BotUttered)
import logging
from twilio.rest import Client
import requests
import json

logging.getLogger(__name__)
class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher, tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("**********************tracker id",tracker.sender_id)

        return [Restarted()]

#class ActionSubmit(Action):

    '''def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("**********************************")
        account_sid = "AC1bff80eafe99e688f521395ccb5df7a0"
        auth_token = "78b7af2b5852a54a8ac3e7ff59c328f7"
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=tracker.get_slot("message"),  #'hello, this is a test message for automation',
            to = "whatsapp:+919913712205"     # '+918209829808'
        )

        print("**********************************",message.sid)

        dispatcher.utter_message(text="Message has been sent successfully to the customer support")

        return []

class ActionSendText(Action):

    def name(self) -> Text:
        return "action_send_text"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="This is a sample text from actions")

        return []

class ActionTalkToHuman(Action):
    def name(self) -> Text:
        return "action_talk_to_human"

    def run(self, dispatcher, tracker, domain):
        response = "Reaching out to a human agent... "#[{}]...".format(tracker.sender_id)
        events=[]
        message="Reaching out to a human agent... "
        ConversationPaused()
        #events.extend(self.redirect_url(message,tracker,dispatcher))
        mes=self.redirect_url(message,tracker,dispatcher)
        print(mes)
        #if mes != "unpause":
        #    dispatcher.utter_message("Human agent: {}".format(message))
        #    self.redirect_url(message,tracker,dispatcher)
        #else:
        #    return [ConversationResumed()]
    
    @staticmethod
    def redirect_url(message,tracker: Tracker,dispatcher):
        dispatcher.utter_message("Human agent: {}".format(message))
        while message != "unpause":
            #url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            #req = requests.get(url)
            #resp = json.loads(req.text)
            #print(resp)
            message = req.json()["message"]
            if "error" in req:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            if message != "unpaused":
                dispatcher.utter_message("Human agent: {}".format(message))
                #message="pause"
                return message
            else:
                return [ConversationResumed()]'''
        

    '''def run(self, dispatcher, tracker, domain):

        # tell the user they are being passed to a customer service agent
        response = "Reaching out to a human agent "#[{}]...".format(tracker.sender_id)
        #print("----------------------------------------1st chatbot is paused---------------------------", tracker.is_paused())
        dispatcher.utter_message(text=response)
        print("-------------------------Inside action default---------------------")
        ConversationPaused()
        tracker.is_paused= True#ConversationPaused()
        #print("----------------------------------------chatbot is paused---------------------------", tracker.is_paused())
        #message="pause"
        #print("----------------------------------MSG-----------------------------------------",message)
        message=""
        if message!="unpaused":
            url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            print("-----------------------------URL----------------------------------------------",url)
            req = requests.get(url)
            print("-----------------------------REQ----------------------------------------------",req.json()["message"])
            resp = json.loads(req.text)
            message = req.json()["message"]
            if "error" in req:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            #message = req.json()["message"]
            #print("-------------------------------message-------------------------------",req.json()["message"])
            if message != "unpaused":
                dispatcher.utter_message("Human agent: {}".format(message))
            while tracker.is_paused==True:
            #print("----------------------------------------get_intent_of_latest_message---------------------------", tracker.get_intent_of_latest_message())
            url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            print("-----------------------------URL----------------------------------------------",url)
            req = requests.get(url)
            print("-----------------------------REQ----------------------------------------------",req.json()["message"])
            resp = json.loads(req.text)
            if "error" in req:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            message = req.json()["message"]
            #print("-------------------------------message-------------------------------",req.json()["message"])
            if message != "unpause":
                print("--------------------------inside IF--------------------")
                print("----------------------------------------chatbot is paused---------------------------", tracker.is_paused)
                dispatcher.utter_message(text="Human agent: {}".format(req.json()["message"]))
                #return [ConversationResumed()]
            else:
                tracker.is_paused=False
                print("-------------------inside else------------------")
                return [ConversationResumed()]
                ("**********************************************","Human agent: {}".format(req.json()["message"]))
            #ConversationResumed()
            #ConversationPaused()
        #return [ConversationPaused()]#,UserUtteranceReverted()]'''

'''class ActionTalkToHuman(Action):
    """
	human in the loop action
	"""

    def name(self):
        return "action_talk_to_human"

    def run(self, dispatcher, tracker, domain):
        response = "Reaching out to a human agent [{}]...".format(tracker.sender_id)
        dispatcher.utter_message(text= {
        "handoff_host": "http://127.0.0.1:5000",
        "title": "Handoff Bot"
        })

        """
		seems like rasa will stop listening once conversation
		is paused, which means no actions are attempted, therefore
		preventing triggering ConversationResumed() in a straightforward way.
		"""
        tracker.update(ConversationPaused())
        message = ""
        while message != "/unpause":
            url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            req = requests.get(url)
            resp = json.loads(req.text)
            if "error" in resp:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            message = resp["message"]
            if message != "/unpause":
                dispatcher.utter_message("Human agent: {}".format(message))

import requests
import json

def pause_conversation(sender_id):
    url = f"http://localhost:5005/conversations/{sender_id}/tracker/events"
    headers = {"Content-Type": "application/json"}
    data = [{"event": "pause"}]

    return requests.post(url=url, data=json.dumps(data), headers=headers)


def resume_conversation(sender_id):
    url = f"http://localhost:5005/conversations/{sender_id}/tracker/events"
    headers = {"Content-Type": "application/json"}
    data = [{"event": "resume"}]

    return requests.post(url=url, data=json.dumps(data), headers=headers)

        tracker.update(ConversationResumed())'''
