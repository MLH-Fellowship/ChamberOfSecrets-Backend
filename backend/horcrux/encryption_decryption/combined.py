from .encryption import encrypt_workflow
from .decryption import decrypt_workflow
from .joining import join
from .splitting import split

def encrypt(filename, out_dir, private_key, username):
    print("inside encrypt")
    encrypted_file=encrypt_workflow(filename,private_key, username)
    print("encryption done")
    split(encrypted_file, out_dir)

def decrypt(filename, in_dir):
    join(in_dir, filename)
    decrypt_workflow(filename)

# choice=int(input("1. Encrypt \n 2. Decrypt"))
# file=input("enter file path")

# if(choice==1):
#     encrypt(file)
# elif(choice==2):
#     decrypt(file)