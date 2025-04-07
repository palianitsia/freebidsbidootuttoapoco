import requests
import re
import json

# URL dell'endpoint
url = "https://tuttoapoco.com/puntate/index.php"

# Funzione per inviare richieste POST
def send_requests():
    promocodes = []
    
    # Intestazioni per la richiesta
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "it-IT,it;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,de;q=0.5,el;q=0.4",
        "Cookie": "_pk_id.2.ce22=a781d8e19095596e.1741598098.; _pk_ses.2.ce22=1",
        "Origin": "https://tuttoapoco.com",
        "Referer": "https://tuttoapoco.com/puntate/index.php"
    }

    # Prima richiesta con l=0
    payload = {
        "s": 1,
        "l": 0
    }
    
    response = requests.post(url, data=payload, headers=headers)
    print(f"Risposta richiesta con s=1 e l=0:", response.status_code)
    
    if response.status_code == 200 and int(response.headers.get('Content-Length', 0)) >= 600:
        try:
            data = json.loads(response.text)  # Carica i dati JSON dalla risposta
            promocodes.extend(extract_promocodes(data))  # Estrai i promocode
        except json.JSONDecodeError:
            print("Errore nel decodificare la risposta JSON.")
    else:
        print("Errore nella richiesta o Content-Length insufficiente:", response.text)

    # Invia richieste con payload specifici
    for l in [10, 20, 30, 40, 50]:  # Invia 10, 20, 30, 40, 50
        payload = {
            "s": 1,
            "l": l  # Imposta il valore di l
        }
        
        response = requests.post(url, data=payload, headers=headers)
        print(f"Risposta richiesta con s=1 e l={l}:", response.status_code)
        
        if response.status_code == 200 and int(response.headers.get('Content-Length', 0)) >= 600:
            try:
                data = json.loads(response.text)  # Carica i dati JSON dalla risposta
                promocodes.extend(extract_promocodes(data))  # Estrai i promocode
            except json.JSONDecodeError:
                print("Errore nel decodificare la risposta JSON.")
        else:
            print("Errore nella richiesta o Content-Length insufficiente:", response.text)

    return promocodes

# Funzione per estrarre i promocode dai dati JSON
def extract_promocodes(data):
    promocodes = []
    for item in data:
        # Estrai la parte dopo "promocode=" e prima di "&"
        match = re.search(r'promocode=(.*?)&', item['link'])
        if match:
            promocodes.append(match.group(1))
    return promocodes

# Funzione principale
def main():
    # Invia le richieste POST e raccogli i promocode
    promocodes = send_requests()
    
    if promocodes:
        with open('./promocodes.txt', 'w') as file:
            for code in promocodes:
                file.write(code + '\n')
        print("Promocodes estratti e salvati in promocodes.txt")
    else:
        print("Nessun promocode trovato.")

# Esegui il bot
if __name__ == "__main__":
    main()
