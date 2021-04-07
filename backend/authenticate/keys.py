from cryptography.fernet import Fernet

def generate_private_key():
    """Method to generate the private key for the user.
    Args-
        None
    Returns-
        private_key::str: Private key of the user.
    """
    private_key = Fernet.generate_key()
    return private_key

def generate_encrypted_public_key(private_key):
    """Method to generate the encrypted public key of the user.
    Args-
        private_key::str: Private key of the user
    Returns-
        encrypted_public_key::str: Encrypted public key of the user
    """
    public_key = Fernet.generate_key()
    f = Fernet(private_key)
    encrypted_public_key = f.encrypt(public_key)
    return encrypted_public_key

