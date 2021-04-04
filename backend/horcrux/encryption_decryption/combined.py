from .encryption import encrypt_workflow
from .decryption import decrypt_workflow
from .joining import join
from .splitting import split

def encrypt(filename, out_dir, private_key, username, split_name):
    encrypted_file = encrypt_workflow(filename, private_key, username)
    split(encrypted_file, out_dir, split_name)

def decrypt(filename, in_dir, private_key, username):
    join(in_dir, filename)
    decrypt_workflow(filename, private_key, username)
