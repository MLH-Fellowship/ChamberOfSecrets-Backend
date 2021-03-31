from cryptography.fernet import Fernet
from authenticate.models import UserInfo

def encrypt_file(filename, public_key):
    f = Fernet(public_key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def get_encryption_key(private_key,encrypted_public_key):
    f = Fernet(private_key)
    public_key = f.decrypt(encrypted_public_key)
    return public_key

def load_keys(req_username):
    #run a query to find public key of user
    current_user=UserInfo.objects.get(username=req_username)
    encrypted_public_key=current_user.public_key
    #load keys from db
    return encrypted_public_key

def encrypt_workflow(filename,private_key, username):
    private_key=bytes(private_key, 'utf-8')
    encrypted_public_key=load_keys(username)
    encrypted_public_key=bytes(encrypted_public_key, 'utf-8')
    public_key=get_encryption_key(private_key,encrypted_public_key)
    encrypt_file(filename,public_key)
    return filename
