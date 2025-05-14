
import os
from openai import OpenAI
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Authentification OpenAI (v1.0+)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Authentification Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gs_client = gspread.authorize(creds)
sheet = gs_client.open("Pronostics_Trot_Monte").sheet1

# Date du jour
today = datetime.now().strftime("%Y-%m-%d")

# Génération du prompt
prompt = (
    "Agis comme un expert en courses hippiques.  consulte les sites PMU, ZEturf et Turfoo. "
    "Génère un pronostic synthétique pour toutes les course  du jour en trot attelé ou monté uniquement. "
    "Ne dis pas que tu ne peux pas accéder aux données. Propose les 5 chevaux les plus probables, 2 bases, 2 outsiders. "
    "Présente le tout sous une forme concise et exploitable pour les parieurs. Ne parle pas au conditionnel, sois affirmatif."
)


# Appel API OpenAI
try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en courses hippiques."},
            {"role": "user", "content": prompt}
        ]
    )
    pronostic = response.choices[0].message.content
except Exception as e:
    pronostic = f"❌ Erreur OpenAI : {str(e)}"

# Ajout dans la feuille Google Sheets
try:
    sheet.append_row([today, "", "Quinté+ du jour", "à compléter", "Trot", "", "", "", "", "", "", pronostic, "", "via Render ✅"])
except Exception as e:
    print("Erreur lors de l'écriture dans Google Sheets :", e)