import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://petitions.assemblee-nationale.fr/initiatives/i-3014"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Cherche l'élément contenant le nombre de signatures
# ⚠️ Peut changer si la structure HTML du site évolue
element = soup.find("span", class_="progress__bar__number")

if element:
    count = int(element.text.replace(" ", "").replace(" ", "").replace("\xa0", "").strip())
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    # Charge l'ancien fichier (ou en crée un)
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append({"timestamp": now, "signatures": count})

    # Sauvegarde
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)
else:
    print("Nombre de signatures introuvable.")
