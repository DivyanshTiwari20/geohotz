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

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import google.generativeai as genai
# import os

# app = Flask(__name__)
# CORS(app)

# # Google Gemini API settings
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# # Initialize the model
# model = genai.GenerativeModel('gemini-pro')

# @app.route('/summarize', methods=['POST'])
# def summarize_text():
#     data = request.get_json()
#     text = data.get('text', '')
    
#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     try:
#         prompt = f"Summarize the following text in a concise manner:\n\n{text}"
#         response = model.generate_content(prompt)
        
#         if response.text:
#             return jsonify({"summary": response.text})
#         else:
#             return jsonify({"error": "No summary generated"}), 500
    
#     except Exception as e:
#         return jsonify({"error": f"An error occurred during summarization: {str(e)}"}), 500

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     message = data.get('message', '')
    
#     if not message:
#         return jsonify({"error": "No message provided"}), 400

#     try:
#         response = model.generate_content(message)
        
#         if response.text:
#             return jsonify({"reply": response.text})
#         else:
#             return jsonify({"error": "No response generated"}), 500
    
#     except Exception as e:
#         return jsonify({"error": f"An error occurred during chat: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)