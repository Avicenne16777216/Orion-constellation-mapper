import requests
import re
import math
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# --- 1. Fonction de conversion des coordonnées stellaires ---
def convertir_coords_stellaires_en_xy(ra_str, dec_str):
    """
    Convertit l'Ascension Droite (RA) et la Déclinaison (Dec)
    en coordonnées x, y en degrés décimaux, en gérant les formats spécifiques de l'API.

    Args:
        ra_str (str): Ascension Droite au format "05h 55m 10.3053s"
        dec_str (str): Déclinaison au format "−08°\xa012′\xa005.9″"

    Returns:
        tuple: (x_coord, y_coord) en degrés décimaux, ou (None, None) si le format est invalide.
    """
    # --- Convertir RA ---
    # Le format RA '05h 14m 32.27s' semble simple
    ra_match = re.match(r'(\d+)h (\d+)m ([\d.]+)s', ra_str)
    if not ra_match:
        # print(f"DEBUG: Format RA non reconnu: '{ra_str}'") # Pour déboguer si besoin
        return None, None
    ra_h, ra_m, ra_s = map(float, ra_match.groups())
    ra_deg = (ra_h + ra_m / 60 + ra_s / 3600) * 15

    # --- Convertir Dec ---
    # Regex pour la déclinaison, incluant l'espace insécable (\s*)
    # et les symboles Unicode spécifiques (minus, prime, double prime)
    dec_match = re.match(r'([+−-])(\d+)°\s*(\d+)′\s*([\d.]+)″', dec_str)
    if not dec_match:
        # print(f"DEBUG: Format Dec non reconnu: '{dec_str}'") # Pour déboguer si besoin
        return None, None
    
    # Le premier groupe est le signe (+ ou − ou -)
    sign_char = dec_match.group(1)
    sign = -1 if sign_char in ['−', '-'] else 1 # Gère les deux types de moins

    # Les groupes suivants sont les valeurs numériques (degrés, minutes, secondes)
    dec_d, dec_m, dec_s = map(float, dec_match.groups()[1:]) 

    dec_deg = sign * (dec_d + dec_m / 60 + dec_s / 3600)
    
    # RA est notre X, Dec est notre Y
    x_coord = ra_deg
    y_coord = dec_deg

    return x_coord, y_coord

# --- 2. Appel à l'API pour récupérer les données des étoiles ---

url_de_base = "https://api.api-ninjas.com/v1/stars"
parametres = {
    "constellation" : "orion"
}

# Load the variables from the .env file
load_dotenv()

# Retrieve the key from the environment
api_key = os.getenv("API_NINJAS_KEY")

headers = {
    'X-Api-Key': api_key # Now the key is hidden!
}

# Listes pour stocker les coordonnées et les noms des étoiles à tracer
all_ra_coords = []
all_dec_coords = []
all_star_names = []

# Noms des étoiles principales d'Orion pour l'annotation sur le graphique
main_stars = [
    "Betelgeuse", "Rigel", "Bellatrix", "Alnilam", 
    "Alnitak", "Mintaka", "Saiph", "Kappa Orionis" # Kappa Orionis est souvent appelée "Saiph" ou "Rigel" B, mais c'est une étoile distincte pour l'API
]

try:
    # Utilise f-string pour l'URL afin d'inclure la constellation directement
    resultats = requests.get(f"{url_de_base}?constellation={parametres['constellation']}", headers=headers)
    resultats.raise_for_status() # Lève une exception pour les codes d'erreur HTTP (4xx ou 5xx)
    etoiles_orion = resultats.json()

    if etoiles_orion:
        print(f"Trouvé {len(etoiles_orion)} étoiles dans Orion (max 30 par requête) :")
        for etoile in etoiles_orion:
            nom = etoile.get('name', 'N/A')
            right_ascension_str = etoile.get('right_ascension', 'N/A')
            declination_str = etoile.get('declination', 'N/A')

            # Convertir les coordonnées
            ra_deg, dec_deg = convertir_coords_stellaires_en_xy(right_ascension_str, declination_str)

            if ra_deg is not None and dec_deg is not None:
                all_ra_coords.append(ra_deg)
                all_dec_coords.append(dec_deg)
                all_star_names.append(nom) # Stocke le nom pour l'annotation
                # print(f"- Nom : {nom}, RA : {ra_deg:.4f}°, Dec : {dec_deg:.4f}°") # Pour vérifier les conversions
            else:
                print(f"Impossible de convertir les coordonnées pour l'étoile : {nom} (RA: '{right_ascension_str}', Dec: '{declination_str}')")
    else:
        print("Aucune étoile n'a été trouvée ! Ou problème avec la requête.")

except requests.exceptions.HTTPError as e:
    print(f"Erreur HTTP : {e}")
    print(f"Réponse de l'API : {resultats.text}")
except requests.exceptions.RequestException as e:
    print(f"Erreur lors de la requête : {e}")
except ValueError:
    print("Erreur de décodage JSON. Le résultat n'est peut-être pas du JSON valide.")

# --- 3. Visualisation avec Matplotlib ---
if all_ra_coords and all_dec_coords: # S'assurer qu'il y a des données à tracer
    plt.figure(figsize=(10, 8)) # Taille du graphique
    plt.scatter(all_ra_coords, all_dec_coords, s=20, color='white', alpha=0.8, edgecolors='none') # Tracer les étoiles

    # Annoter les étoiles principales
    for i, name in enumerate(all_star_names):
        if name in main_stars:
            plt.annotate(name, 
                         (all_ra_coords[i], all_dec_coords[i]), 
                         textcoords="offset points", 
                         xytext=(5,5), 
                         ha='left', 
                         color='yellow', 
                         fontsize=9)

    plt.title("Constellation d'Orion", color='white')
    plt.xlabel("Ascension Droite (Degrés)", color='white')
    plt.ylabel("Déclinaison (Degrés)", color='white')
    
    # Inverser l'axe X pour une représentation astronomique plus courante
    plt.gca().invert_xaxis() 
    
    plt.grid(True, linestyle='--', alpha=0.5) # Ajouter une grille
    plt.gca().set_facecolor('black') # Fond noir pour l'espace
    plt.gcf().set_facecolor('black') # Fond de la figure noir
    plt.tick_params(axis='x', colors='white') # Couleur des graduations X
    plt.tick_params(axis='y', colors='white') # Couleur des graduations Y

    plt.show()
else:
    print("Pas de données d'étoiles valides à tracer.")