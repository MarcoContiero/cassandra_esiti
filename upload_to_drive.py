import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Permessi: solo scrittura su file propri
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def carica_db_su_drive(percorso_db: str):
    creds = None

    # === Step 1: cerca il token già salvato
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        # === Step 2: primo login interattivo (solo da eseguire in locale)
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # === Step 3: costruzione del servizio Drive
    service = build("drive", "v3", credentials=creds)

    # === Step 4: prepara il file da caricare
    nome_file = os.path.basename(percorso_db)
    metadata = {'name': nome_file}
    media = MediaFileUpload(percorso_db, mimetype="application/x-sqlite3")

    # === Step 5: upload
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()
    print(f"✅ File caricato con successo. ID: {file.get('id')}")

if __name__ == "__main__":
    # Percorso del database da caricare (può essere finto per test)
    db_path = "cassandra_analisi.db"

    if os.path.exists(db_path):
        carica_db_su_drive(db_path)
    else:
        print(f"❌ File non trovato: {db_path}")
