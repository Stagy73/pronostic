import os
import json
from datetime import datetime
from openai import OpenAI
import gspread
from oauth2client.service_account import ServiceAccountCredentials

print("📂 Chargement turfoo_data.json...")

# Vérification du fichier JSON
try:
    with open("turfoo_data.json", "r", encoding="utf-8") as f:
        content = f.read()
        if not content.strip():
            raise ValueError("❌ turfoo_data.json est vide.")
        courses = json.loads(content)
        print(f"✅ {len(courses)} course(s) chargée(s)")
except Exception as e:
    print(f"❌ Erreur chargement JSON : {e}")
    exit(1)

# Authentification OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Authentification Google Sheets
print("🔐 Connexion à Google Sheets...")
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    gs_client = gspread.authorize(creds)
    sheet = gs_client.open("Pronostics_Trot_Monte").sheet1
    print("📎 Google Sheet trouvé et ouvert")
except Exception as e:
    print(f"❌ Erreur Google Sheets : {e}")
    exit(1)

# Date du jour
today = datetime.now().strftime("%Y-%m-%d")

# Traitement des courses
for course in courses:
    try:
        hippodrome = course["hippodrome"]
        nom_course = course["nom_course"]
        heure = course["heure"]
        type_course = course["type"]
        chevaux = course["chevaux"]

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

        print(f"🤖 Génération du pronostic pour {nom_course} ({heure})")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en trot attelé et monté."},
                {"role": "user", "content": prompt}
            ]
        )
        pronostic = response.choices[0].message.content
        print(f"✅ Pronostic obtenu pour {nom_course}")

        # Insertion dans Google Sheet
        sheet.append_row([
            today, heure, nom_course, hippodrome, type_course, "", len(chevaux),
            "", "", "", "", pronostic, "", "via Turfoo+GPT"
        ])
        print(f"📤 Ligne ajoutée dans Google Sheets pour {nom_course}")

    except Exception as e:
        print(f"❌ Erreur sur la course {course.get('nom_course', '?')} : {e}")
