from flask import Flask, request, jsonify

app = Flask(__name__)

# Route for testing with GET request from the browser
@app.route('/')
def index():
    return 'The Flask app is running! Use /webhook to send POST requests.', 200

# Webhook endpoint expecting POST requests
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)  # Or process it in other ways
    return jsonify({"status": "success", "data": data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)

