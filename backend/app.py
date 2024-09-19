# from flask import Flask, request, jsonify
# from transformers import pipeline
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # This allows your frontend to access the backend

# # Setup your summarizer
# summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')


# # Define a route for summarization
# @app.route('/summarize', methods=['POST'])
# def summarize_text():
#     data = request.get_json()  # Assuming the request is sending JSON data
#     text = data.get('text', '')
#     summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
#     return jsonify(summary)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Hugging Face API settings
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 150,
                "min_length": 30,
                "do_sample": False
            }
        }
        response = query(payload)
        
        if isinstance(response, list) and len(response) > 0:
            summary = response[0].get('summary_text', '')
            return jsonify({"summary": summary})
        else:
            return jsonify({"error": "Unexpected response from API", "response": response}), 500
    
    except Exception as e:
        return jsonify({"error": f"An error occurred during summarization: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)