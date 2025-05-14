
import requests
from bs4 import BeautifulSoup
import json

def scrape_turfoo_trot():
    url = "https://www.turfoo.fr/programmes-courses/"
    print(f"🌐 Chargement de la page {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Erreur HTTP {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    blocs = soup.select("div.bloc-principal > div.bloc-course")  # structure 2025
    print(f"🔍 {len(blocs)} blocs de course trouvés")

    for bloc in blocs:
        try:
            hippodrome = bloc.find("h2").text.strip()
            rows = bloc.select("table tr.course")

            for row in rows:
                type_text = row.find_all("td")[0].get_text(strip=True).lower()
                if "attelé" in type_text or "monté" in type_text:
                    heure = row.find("td", class_="heure").text.strip()
                    lien = row.find("a")
                    nom_course = lien.text.strip()
                    link = "https://www.turfoo.fr" + lien["href"]

                    print(f"📥 {hippodrome} - {nom_course} ({type_text})")

                    course_resp = requests.get(link)
                    if course_resp.status_code != 200:
                        continue
                    course_soup = BeautifulSoup(course_resp.text, "html.parser")

                    chevaux = []
                    partants = course_soup.select("table.partants tbody tr")
                    for partant in partants:
                        try:
                            num = partant.select_one(".partant").text.strip()
                            nom = partant.select_one(".nom").text.strip()
                            jockey = partant.select_one(".jockey").text.strip()
                            cote = partant.select_one(".cote").text.strip() if partant.select_one(".cote") else "N/A"
                            chevaux.append({
                                "numero": num,
                                "nom": nom,
                                "jockey": jockey,
                                "cote": cote
                            })
                        except:
                            continue

                    results.append({
                        "hippodrome": hippodrome,
                        "nom_course": nom_course,
                        "heure": heure,
                        "type": "trot attelé" if "attelé" in type_text else "trot monté",
                        "url": link,
                        "chevaux": chevaux
                    })
        except Exception as e:
            print(f"❌ Erreur lecture bloc : {e}")
            continue

    print(f"💾 {len(results)} course(s) de trot sauvegardée(s)")
    with open("turfoo_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_turfoo_trot()