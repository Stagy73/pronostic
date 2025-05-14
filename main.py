
import os
import json
from datetime import datetime
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gs_client = gspread.authorize(creds)
sheet = gs_client.open("Pronostics_Trot_Monte").sheet1

# Chargement des données Turfoo
try:
    with open("turfoo_data.json", "r", encoding="utf-8") as f:
        courses = json.load(f)
except Exception as e:
    raise RuntimeError(f"Erreur de lecture de turfoo_data.json : {e}")

# Date du jour
today = datetime.now().strftime("%Y-%m-%d")

# Traitement de chaque course
for course in courses:
    try:
        hippodrome = course["hippodrome"]
        nom_course = course["nom_course"]
        heure = course["heure"]
        type_course = course["type"]
        chevaux = course["chevaux"]

        # Construction du prompt
        prompt_chevaux = "\n".join([
            f"{c['numero']}. {c['nom']} (jockey: {c['jockey']}, cote: {c['cote']})"
            for c in chevaux
        ])

        prompt = (
            f"Analyse la course suivante et donne un pronostic synthétique clair :\n"
            f"Hippodrome : {hippodrome}\n"
            f"Nom : {nom_course}\n"
            f"Heure : {heure}\n"
            f"Type : {type_course}\n"
            f"Participants :\n{prompt_chevaux}\n\n"
            "Donne : les 5 chevaux les plus probables, 2 bases, 2 outsiders. "
            "Sois affirmatif. Format :\nBases : ...\nOutsiders : ...\nSélection : ..."
        )

        # Appel OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en trot attelé et monté."},
                {"role": "user", "content": prompt}
            ]
        )
        pronostic = response.choices[0].message.content

        # Envoi dans Google Sheets
        sheet.append_row([
            today, heure, nom_course, hippodrome, type_course, "", len(chevaux),
            "", "", "", "", pronostic, "", "via Turfoo+GPT"
        ])

    except Exception as e:
        print(f"❌ Erreur sur la course {course.get('nom_course', '?')} : {e}")