from cryptography.fernet import Fernet

def decrypt_file(filename, public_key):
    f = Fernet(public_key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(file_data)
    # write the decrypted file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def get_decryption_key(private_key,encrypted_public_key):
    f = Fernet(private_key)
    public_key = f.decrypt(encrypted_public_key)
    return public_key

def load_keys():
    private_key=open("key.key", "rb").read()
    encrypted_public_key=open("public_key.key", "rb").read()
    return private_key,encrypted_public_key

def decrypt_workflow(filename):
    private_key,encrypted_public_key=load_keys()
    public_key=get_decryption_key(private_key,encrypted_public_key)
    decrypt_file(filename,public_key)
