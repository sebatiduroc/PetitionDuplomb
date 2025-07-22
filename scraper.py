import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://petitions.assemblee-nationale.fr/initiatives/i-3014"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Lève une erreur si code != 200
except requests.RequestException as e:
    print(f"Erreur lors de la récupération de la page : {e}")
    count = None
else:
    soup = BeautifulSoup(response.text, "html.parser")
    # Nouveau sélecteur
    element = soup.find("span", class_="progress__bar__number")

    if element:
        try:
            count = int(
                element.text.replace(" ", "").replace(" ", "").replace("\xa0", "").strip()
            )
        except ValueError:
            print(f"Impossible de convertir '{element.text}' en entier.")
            count = None
    else:
        print("Nombre de signatures introuvable.")
        count = None

# Horodatage
now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# Lecture des anciennes données
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

# Ajout d'une entrée, même si count est None
data.append({"timestamp": now, "signatures": count})

# Sauvegarde
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Ajouté : {now}, signatures = {count}")
