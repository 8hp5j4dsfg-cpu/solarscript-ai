from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import openai
import stripe

app = Flask(__name__)

# === CONFIG ===
stripe.api_key = "sk_test_..."  # REPLACE WITH YOUR KEY LATER
openai.api_key = os.getenv("GROK_KEY")
openai.api_base = "https://api.x.ai/v1"

PRICE_ID = "price_1ABC123..."  # ← PASTE YOUR PRICE ID HERE

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
        result = "Example:\n\n'With the 30% tax credit, your system pays for itself in 6 years — and your bill drops to $0. Want to see your savings?'"
    return jsonify({"script": result})

# === STRIPE CHECKOUT ===
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': PRICE_ID, 'quantity': 1}],
        mode='subscription',
        success_url='https://solarscript-ai.onrender.com/success',
        cancel_url='https://solarscript-ai.onrender.com/'
    )
    return jsonify({'id': session.id})

@app.route('/success')
def success():
    return "<h1>Thanks! Access unlocked. Check email.</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
