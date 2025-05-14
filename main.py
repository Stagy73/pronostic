
import os
import openai
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Authentification OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Authentification Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Pronostics_Trot_Monte").sheet1

# Date du jour
today = datetime.now().strftime("%Y-%m-%d")

# Génération du prompt
prompt = (
    "Fais une synthèse des pronostics du jour pour la course Quinté+ (trot attelé ou monté uniquement), "
    "basée sur PMU, Turfoo et ZEturf. Donne : les 5 chevaux les plus cités, les bases et outsiders, "
    "sous forme claire. Ne donne pas les plats ni galop."
)

# Appel API OpenAI
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert en courses hippiques."},
            {"role": "user", "content": prompt}
        ]
    )
    pronostic = response['choices'][0]['message']['content']
except Exception as e:
    pronostic = f"❌ Erreur OpenAI : {str(e)}"

# Ajout dans la feuille Google Sheets
try:
    sheet.append_row([today, "", "Quinté+ du jour", "à compléter", "Trot", "", "", "", "", "", "", pronostic, "", "via Render ✅"])
except Exception as e:
    print("Erreur lors de l'écriture dans Google Sheets :", e)
