from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    words = request.json
    print("Received words:", words)  # Debugging line to print received data

    # Create a prompt for OpenAI with the given words
    prompt = "Create a fun and engaging story using the following words:\n"
    for word_type, word_list in words.items():
        prompt += f"{word_type}: {', '.join(word_list)}\n"

    prompt += "\nStory:"

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    story = response.choices[0].message.content.strip()
    return jsonify({"story": story})

if __name__ == '__main__':
    app.run(debug=True)