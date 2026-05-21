from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GROQ_API_KEY = "TU_GROQ_API_KEY"

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.json

    prompt = f"""
    Clasifica este mensaje en:
    - Intención
    - Urgencia (alta, media, baja)
    - Prioridad (1 a 5)
    - Resumen breve

    Datos:
    Nombre: {data['nombre']}
    Email: {data['email']}
    Teléfono: {data['telefono']}
    Mensaje: {data['mensaje']}
    """

    ai_payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Eres un analista experto."},
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    ai_response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=ai_payload,
        headers=headers
    )

    texto = ai_response.json()["choices"][0]["message"]["content"]

    return jsonify({
        "intencion": texto,
        "urgencia": texto,
        "prioridad": texto,
        "resumen": texto
    })

@app.route("/", methods=["GET"])
def home():
    return "API funcionando"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
