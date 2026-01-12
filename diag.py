import requests
import json

# Configuration à tester (Mets ici l'IP du Membre 2 pour tester)
TARGET_IP = "10.100.126.84" 
TARGET_PORT = 5002
MEMBER_NAME = "Member NI"

url = f"http://{TARGET_IP}:{TARGET_PORT}"

print(f"--- TEST DIAGNOSTIC VERS {MEMBER_NAME} ({url}) ---")

# 1. Test de connexion basique (Health)
try:
    print(f"1. Tentative de connexion /health...")
    r = requests.get(f"{url}/health", timeout=5)
    print(f"   CODE: {r.status_code}")
    print(f"   REPONSE: {r.text}")
except Exception as e:
    print(f"   ERREUR FATALE: {e}")
    exit()

# 2. Test d'inférence (Ollama via Python)
try:
    print(f"\n2. Tentative de génération (Question simple)...")
    payload = {"query": "Say hello briefly"}
    # On met un timeout court pour voir si ça accroche
    r = requests.post(f"{url}/answer", json=payload, timeout=10)
    
    if r.status_code == 200:
        print(f"   SUCCÈS ! Réponse :")
        print(f"   {r.json()}")
    else:
        print(f"   ÉCHEC (Code {r.status_code})")
        print(f"   Détail: {r.text}")
        
except Exception as e:
    print(f"   ERREUR D'ENVOI: {e}")