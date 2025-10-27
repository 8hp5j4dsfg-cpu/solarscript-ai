from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

# Use Grok via OpenAI-compatible proxy (we'll fix API later)
openai.api_key = os.getenv("GROK_KEY")
openai.api_base = "https://api.x.ai/v1"  # Grok endpoint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = f"""
    You are a top solar appointment setter.
    Objection: "{data['objection']}"
    Lead: {data['temp']}, Bill: ${data['bill']}/mo
    Write:
    1. 60-sec rebuttal (natural)
    2. 15-sec voicemail
    3. 1 SMS
    Confidence (1-10):
    """
    try:
        response = openai.ChatCompletion.create(
            model="grok-beta",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
    except:
        result = "API not connected yet. Example:\n\n'Actually, with the 30% tax credit, your system pays for itself in 6 years — and your bill drops to $0. Want to see your custom savings?'"
    return jsonify({"script": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
