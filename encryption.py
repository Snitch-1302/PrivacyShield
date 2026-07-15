"""
encryption.py

Symmetric encryption/decryption of location data at rest or in transit,
using Fernet (AES-128 in CBC mode with HMAC authentication).

Note: this protects data confidentiality once it's already been
anonymized/obfuscated by the other modules -- encryption and anonymization
solve different problems. Encryption keeps data unreadable to anyone
without the key; anonymization (cloaking.py, differential_privacy.py)
protects against inference even by parties who *can* read the data.
"""

from cryptography.fernet import Fernet


def generate_key():
    """Generate a new Fernet symmetric key. Store this securely -- anyone
    with this key can decrypt any location encrypted with it."""
    return Fernet.generate_key()


def encrypt_location_data(location, key):
    """Encrypt a (lat, lon) tuple into bytes."""
    location_str = f"{location[0]},{location[1]}"
    fernet = Fernet(key)
    return fernet.encrypt(location_str.encode())


def decrypt_location_data(encrypted_location, key):
    """Decrypt bytes back into a (lat, lon) tuple."""
    fernet = Fernet(key)
    decrypted_location = fernet.decrypt(encrypted_location).decode()
    lat, lon = map(float, decrypted_location.split(","))
    return (lat, lon)
