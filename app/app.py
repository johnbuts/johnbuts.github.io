from flask import Flask, jsonify, request
import requests
import threading
import time
import json

# Initialize the Flask application
app = Flask(__name__)
storage = {}
OLLAMA_API_URL = 'http://127.0.0.1:11434/api/chat'
# Function that the thread will execute
def ask_ollama(thread_id, latest_message):
    headers = {
        "Content-Type": "application/json"
    }
    messages = []
    if thread_id in storage:
        messages = storage[thread_id]
    
    messages.append(
        {
            'role' : 'user',
            'content' : latest_message
        }
    )
    data = {
        'model': r'gemma2:2b',
        'messages': messages,
        'stream': False
    }
    json_data = json.dumps(data)
    json_data = json_data.replace('False', 'false')
    print(json_data)
    response = requests.post(OLLAMA_API_URL, json=json.loads(json_data), headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        llama_message = response_json['message']['content']
        messages.append(
            {
                "role" : "assistant",
                "content" : llama_message
            }
        )
        storage[thread_id] = messages
    else:
        return f"Error: {response.status_code}, {response.text}"

    return llama_message
    

# Endpoint to start a new thread
@app.route('/api/start-thread', methods=['POST'])
def start_thread():
    # Get JSON data from the request body
    print(request.get_json())
    data = request.get_json()
    
    # Check if 'id' is present in the request body
    if 'id' not in data:
        return jsonify({"error": "Missing 'id' in request body"}), 400

    thread_id = data['id']
    user_message = data['message']

    new_message = ask_ollama(thread_id, user_message)

    return jsonify({"message": new_message}), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)