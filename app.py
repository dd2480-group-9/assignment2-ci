"""
This module provides 2 methods for server handling and HTTP interaction using flask framework
"""


from flask import Flask, request, jsonify   # Importing flask 
import json                                 # Importing json

app = Flask(__name__)  # Creates one instance of flask

# Defining the initial route
@app.route('/')
def index():
    
    return 'Hello Group 9' # Output on HTTP page 


# Route that reacts when someone tries to access the /webhook on a browser. 
@app.route('/webhook', methods=['GET'])
def webhook():
    if request.method == 'GET':  
        print("GET request received!")  
        return 'You are now in a different route, Congrats !'
    
# Route that reacts when "input" is given such as webhooks or requests
@app.route('/webhook', methods=['POST'])
def post_webhook():
 
    if request.method == 'POST':  
        print("POST request received!")  
        return jsonify({'message': 'POST request received on /webhook'}), 200  

# Running the server instance via run command. 
if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0') 
