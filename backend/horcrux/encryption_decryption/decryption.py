from cryptography.fernet import Fernet
from authenticate.models import UserInfo

def decrypt_file(filename, public_key):
    """Method to decrypt a file
    Args- 
        filename::str: Path of the file
        public_key::str: Public key of the user
    Returns-
        None  
    """
    f = Fernet(public_key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(file_data)
    # write the decrypted file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def get_decryption_key(private_key, encrypted_public_key):
    """Method to decrypt the encrypted public key using the user's private key.
    Args-
        private_key::str: Private key of the user
        encrypted_public_key::str: User's encrypted key from the database
    Returns-
        public_key::str: Public key of the user
    """
    f = Fernet(private_key)
    public_key = f.decrypt(encrypted_public_key)
    return public_key

def load_keys(req_username):
    """Method to fetch user's encrypted public key from the database.
    Args-
        req_username::str: Username of the user
    Returns-
        encrypted_public_key::str: Encrypted public key of the user
    """
    # run a query to find public key of user
    current_user = UserInfo.objects.get(username=req_username)
    encrypted_public_key = current_user.public_key
    # load keys from db
    return encrypted_public_key

def decrypt_workflow(filename, private_key, username):
    """Method to integrate the entire file encryption workflow.
    Args-
        filename::str: Name(path) of the file
        private_key::str: Private key of the user
        username::str: Username of the user
    Returns-
        None
    """
    private_key = bytes(private_key, "utf-8")
    encrypted_public_key = load_keys(username)
    encrypted_public_key = bytes(encrypted_public_key, "utf-8")
    public_key = get_decryption_key(private_key, encrypted_public_key)
    decrypt_file(filename, public_key)
