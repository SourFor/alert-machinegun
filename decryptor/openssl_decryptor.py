import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def derive_key_and_iv(password, salt, key_length, iv_length, iterations=100000):
    """Derive key and IV using PBKDF2."""
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length + iv_length,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    key_iv = kdf.derive(password.encode('utf-8'))
    return key_iv[:key_length], key_iv[key_length:key_length + iv_length]

def decrypt_openssl_file(file_path, password):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    # Decode the base64 encoded data
    encrypted_data = base64.b64decode(encrypted_data)

    # Extract the salt from the encrypted file
    if encrypted_data[:8] != b'Salted__':
        raise ValueError("Missing salt header")
    salt = encrypted_data[8:16]  # Salt is in bytes 8-16
    encrypted = encrypted_data[16:]  # The rest is the actual encrypted data

    # Derive key and IV from the password and salt
    key, iv = derive_key_and_iv(password, salt, 32, 16, iterations=100000)
    
    # Decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode('utf-8')
