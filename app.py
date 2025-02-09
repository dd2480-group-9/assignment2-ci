from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')

def index():
    return 'Hello Group 9'
if __name__ == '__main__':
    app.run(debug=True, port = 8009, host='0.0.0.0')  # Should be hosted on port 80 + group 9 = 8009


