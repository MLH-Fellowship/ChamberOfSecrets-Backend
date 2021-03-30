from cryptography.fernet import Fernet

def generate_private_key():
    private_key = Fernet.generate_key()
    return private_key

def generate_encrypted_public_key(private_key):
    public_key = Fernet.generate_key()
    f = Fernet(private_key)
    encrypted_public_key = f.encrypt(public_key)
    return encrypted_public_key

