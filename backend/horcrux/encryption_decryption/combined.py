from .encryption import encrypt_workflow
from .decryption import decrypt_workflow
from .joining import join
from .splitting import split

def encrypt(filename, out_dir, private_key, username, split_name):
    """Method for file encryption and splitting into horcruxes.
    Args-
        filename::str: Name(path) of the file to be encrypted
        out_dir::str: Path of the directory where splits are to be made
        private_key::str: Private key of the user
        username::str: Username of the user
        split_name::str: Identifier of the splits
    Returns-
        None
    """
    encrypted_file = encrypt_workflow(filename, private_key, username)
    split(encrypted_file, out_dir, split_name)

def decrypt(filename, in_dir, private_key, username):
    """Method for file recombination of horcruxes into a file and decryption.
    Args-
        filename::str: Name(path) of the file to be Decrypted
        in_dir::str: Path of the directory where horcruxes are located
        private_key::str: Private key of the user
        username::str: Username of the user
    """
    join(in_dir, filename)
    decrypt_workflow(filename, private_key, username)
