from google.cloud import storage
from google.oauth2 import service_account
import io

# Usa credenziali dal file già caricato (es. 'credentials.json' su Railway)
CREDENTIALS_FILE = "credentials.json"

def upload_to_gcs(bucket_name, gcs_path, data, content_type="application/json"):
    """
    Carica dati (in bytes) su GCS nel percorso indicato.

    :param bucket_name: Nome del bucket (es: "cassandra_backup_moire")
    :param gcs_path: Percorso nel bucket (es: "previsioni/file.json")
    :param data: Oggetto bytes o string (JSON, CSV, ecc.)
    :param content_type: Tipo MIME (default: JSON)
    """
    if isinstance(data, str):
        data = data.encode("utf-8")

    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE)
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    blob.upload_from_file(io.BytesIO(data), size=len(data), content_type=content_type)
    print(f"✅ Caricato su GCS: gs://{bucket_name}/{gcs_path}")
