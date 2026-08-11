import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from database.config import settings


KEY = hashlib.sha256(
    settings.BYTEVAULT_ENCRYPTION_KEY.encode()
).digest()


def encrypt(data: bytes) -> bytes:
    nonce = os.urandom(12)

    encrypted_data = AESGCM(KEY).encrypt(
        nonce,
        data,
        None,
    )

    return nonce + encrypted_data


def decrypt(data: bytes) -> bytes:
    nonce = data[:12]
    encrypted_data = data[12:]

    return AESGCM(KEY).decrypt(
        nonce,
        encrypted_data,
        None,
    )