import json
from flask import Flask, request, render_template, Response, jsonify
import json
import logging

app = Flask(__name__, template_folder='template')

@app.route('/display_message', methods=['GET'])
def display_message():
    print("Hello")
    return {"1":"1"}

@app.route('/',methods=['GET'])
def index():
    return render_template('display_message.html')

if __name__ == '__main__':
    app.run(port=6001,debug=True)
