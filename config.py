# config.py
import base64
import hashlib
from cryptography.fernet import Fernet

class Config:
    DEFAULT_HOST = "201.51.106.6"
    DEFAULT_PORT = 7444
    # Gera uma chave válida de 32 bytes e converte para Base64
    ENCRYPTION_KEY = base64.urlsafe_b64encode(hashlib.sha256(b'qweasd').digest())
    CIPHER_SUITE = Fernet(ENCRYPTION_KEY)