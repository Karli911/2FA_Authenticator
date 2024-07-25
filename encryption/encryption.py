import os
from cryptography.fernet import Fernet, InvalidToken

def generate_encryption_key():
    return Fernet.generate_key()

def load_encryption_key(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            key = file.read()
    else:
        key = generate_encryption_key()
        with open(file_path, 'wb') as file:
            file.write(key)
    return key

def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data).decode()
    except InvalidToken:
        raise ValueError("Invalid encryption key or corrupted data.")
    return decrypted_data