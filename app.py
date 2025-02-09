from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello Group 9'
if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0')  # Should be hosted on port 80 + group 9 = 8009

@app.route('/webhook', methods=['GET'])
def webhook():
    if request.method == 'GET':  
        print("GET request received!")  
        return 'You are now in a different route, Congrats !'
    
@app.route('/webhook', methods=['POST'])
def post_webhook():
 
    if request.method == 'POST':  
        print("POST request received!")  
        return jsonify({'message': 'POST request received on /webhook'}), 200  

if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0') 
