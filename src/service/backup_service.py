"""Serviço de backup do banco de dados."""

import os
import zipfile
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "data.json")
BACKUP_DIR = os.path.dirname(DB_PATH)


def generate_backup() -> str | None:
    """Gera um backup zip do data.json. Retorna o nome do arquivo ou None se falhar."""
    if not os.path.exists(DB_PATH):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"backup_{timestamp}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(DB_PATH, "data.json")

    return zip_name
