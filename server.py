import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

# Charger la base de connaissance en mémoire au démarrage
with open('knowledge.txt', 'r', encoding='utf-8') as f:
    SYSTEM_CONTEXT = f.read()

# Vérification de la clé API
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("La variable d'environnement MISTRAL_API_KEY n'est pas définie.")

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MODEL = "mistral-small"  # ou "mistral-medium"

@app.route('/')
def index():
    """Servir la page HTML principale."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Proxy vers l'API Mistral avec injection du contexte système."""
    data = request.get_json()
    if not data or 'messages' not in data:
        return jsonify({"error": "Format de requête invalide. Attendu : { messages: [...] }"}), 400

    user_messages = data['messages']
    
    # Construction du tableau complet avec le système en premier
    full_messages = [
        {"role": "system", "content": SYSTEM_CONTEXT}
    ] + user_messages

    # Limitation optionnelle de l'historique : garder les 20 derniers messages + système
    # full_messages = full_messages[:1] + full_messages[-20:]

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": full_messages,
        "temperature": 0.3,
        "max_tokens": 1024
    }

    try:
        response = requests.post(MISTRAL_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        mistral_data = response.json()
        assistant_message = mistral_data['choices'][0]['message']
        return jsonify({"message": assistant_message})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Erreur API Mistral : {e}")
        return jsonify({"error": "Désolé, une erreur est survenue lors de l'appel à l'IA."}), 502

if __name__ == '__main__':
    # En local uniquement
    app.run(debug=True, host='0.0.0.0', port=5000)