from cryptography.fernet import Fernet
import sys
import os

key_file = sys.argv[1]
key1 = open(key_file, "rb").read()
f = Fernet(key1)
file = sys.argv[2]

data = open(file, "rb").read()

encrypted_data = f.encrypt(data)

with open(file + ".encrypted", "wb") as f:
    f.write(encrypted_data)

    os.remove(file)

print("file encrypted")




