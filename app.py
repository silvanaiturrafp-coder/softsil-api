from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

GROQ_API_KEY = "TU_GROQ_API_KEY"

SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

class WebhookData(BaseModel):
    nombre: str
    email: str
    telefono: str
    mensaje: str

@app.get("/")
def home():
    return {"status": "API funcionando correctamente"}

@app.post("/webhook")
async def webhook(data: WebhookData):

    # Cargar credenciales SOLO cuando se llama al webhook
    CREDS = ServiceAccountCredentials.from_json_keyfile_name(
        "service_account.json", SCOPE
    )
    gc = gspread.authorize(CREDS)
    sheet = gc.open("SOFTSIL_CLIENTES").sheet1

    # --- resto del código ---
