from cryptography.fernet import Fernet
from authenticate.models import UserInfo

def encrypt_file(filename, public_key):
    """Method to encrypt a given file using a public key.
    Args-
        filename::str: Name(path) of the file the is to be encrypted
        public_key::str: Public key of the user
    Returns-
        None
    """
    f = Fernet(public_key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def get_encryption_key(private_key, encrypted_public_key):
    """Method to decrypt the public key of the user.
    Args-
        private_key::str: Private key of the user
        encrypted_public_key::str: Encrypted public key of the user
    Returns-
        public_key::str: Decrpypted public key of the user
    """
    f = Fernet(private_key)
    public_key = f.decrypt(encrypted_public_key)
    return public_key

def load_keys(req_username):
    """Method to load the encrypted public key of the user from the database.
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

def encrypt_workflow(filename, private_key, username):
    """Method to integrate the entire encryption workflow.
    Args-
        filename::str: Name(path) of the file to be encrypted
        private_key::str: Private key of the user
        username::str: Username of the user
    """
    private_key = bytes(private_key, 'utf-8')
    encrypted_public_key = load_keys(username)
    encrypted_public_key = bytes(encrypted_public_key, 'utf-8')
    public_key = get_encryption_key(private_key, encrypted_public_key)
    encrypt_file(filename, public_key)
    return filename
