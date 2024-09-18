from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows your frontend to access the backend

# Setup your summarizer
summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')


# Define a route for summarization
@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()  # Assuming the request is sending JSON data
    text = data.get('text', '')
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return jsonify(summary)

if __name__ == '__main__':
    app.run(debug=True)
