import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def get_cipher():
    key = os.environ.get("AES_KEY", "").encode()
    iv = os.environ.get("AES_IV", "").encode()

    if len(key) != 16 or len(iv) != 16:
        raise ValueError("AES_KEY and AES_IV must be 16 bytes each")

    return Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

def encrypt_file(input_path, output_path):
    cipher = get_cipher()
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
        f_out.write(encryptor.update(f_in.read()) + encryptor.finalize())