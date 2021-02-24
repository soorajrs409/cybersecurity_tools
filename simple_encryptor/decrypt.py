from cryptography.fernet import Fernet
import sys
import os

key_file = sys.argv[1]
file = sys.argv[2]

key = open("key1.key", "rb").read()
f = Fernet(key)

file_data = open(file, "rb").read()

decrypted_data = f.decrypt(file_data)
file_name = file.split(".")

with open(file_name[0] + "." + file_name[-2], "wb") as f:
    f.write(decrypted_data)
    os.remove(file)

print("file decrypted")
