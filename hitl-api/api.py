import time
from flask import Flask, jsonify, request
import requests
import json
app = Flask(__name__)
from rasa_sdk import Action, Tracker
import json
import logging
import rasa.core.channels.channel
import requests
import sanic
import sanic.response

@app.route("/")
def hello():
    return "hello, bots"

@app.route("/incomingmessage" , methods=["GET"])
def incomingmessage():
    if request.method == "POST":
        data=request.json
        print(data)
    return data


#meetup_store = {"toronto": {"tech": [251176370]}}

'''
@app.route("/meetup/<location>/<m_type>", methods=["GET", "POST"])
def meetup(location, m_type):
    if request.method == "POST":
        """
        POST
        add meetup id to meetup store
        """
        if location in meetup_store:
            if m_type in meetup_store[location]:
                meetup_store[location][m_type].append(request.data.meetup_id)
            else:
                meetup_store[location][m_type] = []
                meetup_store[location][m_type].append(request.data.meetup_id)
        else:
            meetup_store[location] = {}
            meetup_store[location][m_type] = []
            meetup_store[location][m_type].append(request.data.meetup_id)
    else:
        """
        GET
        retry 10 times with 10 sec sleeps to fetch info
        """
        # emulate slow response
        time.sleep(5)
        if location in meetup_store and m_type in meetup_store[location]:
            return jsonify({"meetup_id": meetup_store[location][m_type]})
        else:
            return jsonify({"error": "no meetups found"})


"""
stores senders and state of chat
{
    [sender_id]: {
        paused: True | False,
        replies: [],
    }
}
"""
'''
sender_store = {"918758914438": {"paused": True, "replies": []}}

@app.route("/handoff/<sender_id>", methods=["GET", "POST"])
def handoff(sender_id):
    if request.method == "POST":
        """
        POST
        add sender id to sender store
        """
        print("---------------------Inside IF----------------------", sender_store)
        print("---------------------json------------------",request.json)
        print("------------------sender------------------",sender_id)
        if sender_id in sender_store:
            #print("-------------sender message--------------",request.get_json()["message"])
            sender_store[sender_id]["replies"].append(request.get_json()["message"])#[0]['text']['body'])
            #print("---------------------------------jsonify(sender_store[sender_id])-------------------------",jsonify(sender_store[sender_id]))
            return jsonify(sender_store[sender_id])
        else:
            return jsonify({"error": "sender_id not found"})
    else:
        """
        GET
        retry 10 times with 10 sec sleeps to fetch info
        """
        print("-----------------------Inside else-------------------------",sender_store )
        if sender_id not in sender_store:
            sender_store[sender_id] = {"paused": True, "replies": []}

        ## poll on replies to fetch the message
        while len(sender_store[sender_id]["replies"]) == 0:
            time.sleep(1)

        message = sender_store[sender_id]["replies"].pop(0)
        print("-----------------------else msg-----------------",message)
        return jsonify({"message": message})
        #return jsonify(sender_store[sender_id])


if __name__ == "__main__":
    app.run(host=app.config.get("HOST"), port=app.config.get("PORT"), debug=True)

