
import requests
import re
import json
from bs4 import BeautifulSoup

def scrape_turfoo_text_based():
    url = "https://www.turfoo.fr/programmes-courses/"
    print(f"🌐 Chargement de la page {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Erreur HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n")

    pattern = re.compile(
        r"(C\d+.*?)\n(\d{2}:\d{2}) • (Trot attelé|Trot monté|Haies|Steeple-chase) • (\d+) Partants",
        re.IGNORECASE
    )

    matches = pattern.findall(text)
    print(f"🔍 {len(matches)} course(s) détectée(s) via texte")

    results = []
    for nom_brut, heure, discipline, partants in matches:
        course = {
            "nom_course": nom_brut.strip(),
            "heure": heure,
            "discipline": discipline.lower(),
            "partants": int(partants),
            "chevaux": [],  # non disponibles en scraping brut
        }
        print(f"📥 {heure} - {nom_brut.strip()} ({discipline}, {partants} partants)")
        results.append(course)

    print(f"💾 Sauvegarde dans turfoo_data.json")
    with open("turfoo_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_turfoo_text_based()