from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import gspread
from google.oauth2.service_account import Credentials


scope = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(credentials)

sheet = client.open("datasheet softsil").worksheet("Hoja 1")

app = FastAPI()

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
GROQ_API_KEY = "TU_GROQ_API_KEY"

# Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    "service_account.json", SCOPE
)

gc = gspread.authorize(CREDS)
sheet = gc.open("SOFTSIL_CLIENTES").sheet1


# -----------------------------
# MODELO DE DATOS
# -----------------------------
class WebhookData(BaseModel):
    nombre: str
    email: str
    telefono: str
    mensaje: str


# -----------------------------
# RUTA PRINCIPAL
# -----------------------------
@app.get("/")
def home():
    return {"status": "API funcionando correctamente"}


# -----------------------------
# WEBHOOK PRINCIPAL
# -----------------------------
@app.post("/webhook")
async def webhook(data: WebhookData):

    prompt = f"""
    Clasifica este mensaje en:
    - Intención
    - Urgencia (alta, media, baja)
    - Prioridad (1 a 5)
    - Resumen breve

    Datos:
    Nombre: {data.nombre}
    Email: {data.email}
    Teléfono: {data.telefono}
    Mensaje: {data.mensaje}
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

    # Guardar en Google Sheets
    sheet.append_row([
        data.nombre,
        data.email,
        data.telefono,
        data.mensaje,
        texto
    ])

    return {
        "status": "ok",
        "clasificacion": texto
    }

