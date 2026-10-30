"""
Storage adapter supporting Vercel Blob private storage and local development disk fallback.
Never exposes raw private Blob URLs or tokens to unauthorized clients.
"""
import os
import uuid
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import logger


class StorageAdapter:
    def __init__(self):
        self.blob_token = settings.BLOB_READ_WRITE_TOKEN
        self.local_dir = os.path.abspath(settings.LOCAL_STORAGE_DIR)
        os.makedirs(self.local_dir, exist_ok=True)

    def save_file(self, content: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """Saves file to Vercel Blob if token is set, else saves to local storage directory."""
        safe_filename = f"{uuid.uuid4().hex}_{os.path.basename(filename)}"

        if self.blob_token:
            # Vercel Blob upload via REST API
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {self.blob_token}",
                    "x-content-type": mime_type,
                    "x-add-random-suffix": "false",
                }
                url = f"https://blob.vercel-storage.com/{safe_filename}"
                resp = requests.put(url, data=content, headers=headers, timeout=10)
                if resp.status_code in [200, 201]:
                    data = resp.json()
                    return {
                        "storage_path": data.get("url", safe_filename),
                        "storage_provider": "vercel_blob",
                        "safe_filename": safe_filename,
                    }
                else:
                    logger.warning(f"Vercel Blob upload failed with status {resp.status_code}, falling back to local")
            except Exception as e:
                logger.warning(f"Vercel Blob upload exception: {e}, falling back to local storage")

        # Local storage adapter fallback
        file_path = os.path.join(self.local_dir, safe_filename)
        with open(file_path, "wb") as f:
            f.write(content)

        return {
            "storage_path": f"local://{safe_filename}",
            "storage_provider": "local_disk",
            "safe_filename": safe_filename,
        }

    def delete_file(self, storage_path: str) -> bool:
        """Removes stored file from Vercel Blob or local storage."""
        if storage_path.startswith("local://"):
            filename = storage_path.replace("local://", "")
            file_path = os.path.join(self.local_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        elif self.blob_token and storage_path.startswith("http"):
            try:
                import requests
                headers = {"Authorization": f"Bearer {self.blob_token}"}
                requests.delete(storage_path, headers=headers, timeout=5)
                return True
            except Exception as e:
                logger.warning(f"Failed deleting blob {storage_path}: {e}")
        return False


storage_service = StorageAdapter()

