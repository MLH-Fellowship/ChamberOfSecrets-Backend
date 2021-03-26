from cryptography.fernet import Fernet
from fsplit.filesplit import Filesplit
import os

'''
Instructions to test:
Generate a key using crypto.py in authenticate folder
1. To encrypt a file, run python horcrux.py filename or path/to/filepath(if not in same directory) -e --dir="path to output directory where horcruxes are saved"
2. To merge the split files, run python horcrux.py filename/filepath -m --dir="path to directory where horcruxes were saved"
3. To decrypt file, run python horcrux.py path/to/file -d
'''

fs = Filesplit()


def split_cb(f, s):
    print("file: {0}, size: {1}".format(f, s))

def merge_cb(f, s):
    print("file: {0}, size: {1}".format(f, s))

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(fileDir, '../authenticate/key.key')
    filename = os.path.abspath(os.path.realpath(filename))
    return open(filename, "rb").read()

def encrypt(filename, key, out_dir):
    """
    Given a filename (str) and key (bytes), it encrypts the file and divides it into horcruxes and saves it to output directory
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

    fs.split(file=filename, split_size=900000, output_dir=out_dir, callback=split_cb)

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def merge(in_dir):
    fs.merge(input_dir=in_dir, callback=merge_cb)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Encryptor Script")
    parser.add_argument("file", help="File to encrypt/decrypt")
    parser.add_argument("-e", "--encrypt", action="store_true",
                        help="Whether to encrypt the file, only -e or -d can be specified.")
    parser.add_argument("-d", "--decrypt", action="store_true",
                        help="Whether to decrypt the file, only -e or -d can be specified.")
    parser.add_argument("-m", "--merge", action="store_true",
                        help="merge divided files")
    parser.add_argument("--dir",help="directory where parts of file are stored")                    

    args = parser.parse_args()
    file = args.file
    # load the key
    key = load_key()

    encrypt_ = args.encrypt
    decrypt_ = args.decrypt
    merge_ = args.merge

    if encrypt_ and decrypt_:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")
    elif encrypt_:
        out_dir = args.dir
        encrypt(file, key, out_dir)
    elif decrypt_:
        decrypt(file, key)
    elif merge:
        in_dir = args.dir
        merge(in_dir)
    else:
        raise TypeError("Please specify whether you want to encrypt the file or decrypt it.")