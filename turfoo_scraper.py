
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def scrape_turfoo_trot():
    url = "https://www.turfoo.fr/programmes-courses/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    reunions = soup.find_all("div", class_="bloc-course")
    for reunion in reunions:
        try:
            hippodrome = reunion.find("h2").text.strip()
            tables = reunion.find_all("table")

            for table in tables:
                row = table.find("tr", class_="course")
                type_text = row.find("td").get_text(strip=True).lower()

                if "attelé" in type_text or "monté" in type_text:
                    heure = row.find("td", class_="heure").text.strip()
                    nom_course = row.find("a").text.strip()
                    link = "https://www.turfoo.fr" + row.find("a")["href"]

                    course_page = requests.get(link)
                    course_soup = BeautifulSoup(course_page.text, "html.parser")

                    chevaux = []
                    for tr in course_soup.select("table.partants tbody tr"):
                        try:
                            num = tr.select_one(".partant").text.strip()
                            nom = tr.select_one(".nom").text.strip()
                            jockey = tr.select_one(".jockey").text.strip()
                            cote = tr.select_one(".cote").text.strip() if tr.select_one(".cote") else "N/A"
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
        except:
            continue

    with open("turfoo_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_turfoo_trot()
