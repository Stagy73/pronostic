
import os
import openai
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Pronostics_Trot_Monte").sheet1

# Date
today = datetime.now().strftime("%Y-%m-%d")

# Génération du prompt
prompt = (
    "Donne-moi un pronostic synthétique pour la course Quinté+ du jour (trot attelé ou monté uniquement), "
    "avec les informations des sites PMU, ZEturf, Turfoo. Indique les 5 chevaux principaux, les bases et outsiders."
)

# Appel OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Tu es un expert en courses hippiques."},
        {"role": "user", "content": prompt}
    ]
)

pronostic = response['choices'][0]['message']['content']

# Insertion dans Google Sheets
sheet.append_row([today, "", "Quinté du jour", "Lieu à préciser", "Trot", "", "", "", "", "", "", pronostic, "", "Auto Render OpenAI"])
