import os
from cryptography.fernet import Fernet
import sys

path = sys.argv[2]
key_file = open(sys.argv[1], "rb").read()


def encrypt_file(key, file):
    f = Fernet(key)
    data = open(file, "rb").read()
    encrypted_data = f.encrypt(data)
    with open(file + ".encrypted", "wb") as fl:
        fl.write(encrypted_data)
        os.remove(file)


files = []
if os.path.isfile(path):
    print("encrypted file ")
    encrypt_file(key_file, path)
    exit()


elif os.path.isdir(path):
    # print("THE BELOW MENTIONED FILES WILL BE ENCRYPTED")
    for (root, dirs, file_names) in os.walk(path):
        for i in file_names:
            files.append(os.path.abspath(os.path.join(root, i)))

else:
    print("error occured. please check the path")
    exit()

# print("THE BELOW MENTIONED FILES WILL BE ENCRYPTED")
for i in files:
    print(i)
print("\nTHE ABOVE MENTIONED FILES WILL BE ENCRYPTED\n")

choice = input("type yes to encrypt : ")
print("\n")
if choice.lower() == "yes":
    for i in files:
        print("encrypting : ", i)
        encrypt_file(key_file, i)

print("\nALL FILE ARE ENCRYPTED ")

if choice.lower() == "no":
    print("aborting the program, bye...")
    exit()

