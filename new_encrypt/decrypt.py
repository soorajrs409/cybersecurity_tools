import os
from cryptography.fernet import Fernet
import sys

path = sys.argv[2]
key_file = open(sys.argv[1], "rb").read()


def decrypt_file(key, file):
    f = Fernet(key)
    file_data = open(file, "rb").read()
    decrypted_data = f.decrypt(file_data)
    file_name = file.split(".")
    try:
        with open(file_name[0] + "." + file_name[-2], "wb") as fl:
            fl.write(decrypted_data)
            os.remove(file)
    except:
        with open(file_name[0], "wb") as fl:
            fl.write(decrypted_data)
            os.remove(file)


files = []
if os.path.isfile(path):
    print("decrypted file")
    decrypt_file(key_file, path)
    exit()


elif os.path.isdir(path):
    for (root, dirs, file_names) in os.walk(path):
        for i in file_names:
            files.append(os.path.abspath(os.path.join(root, i)))

else:
    print("error occured. please check the path")
    exit()

for i in files:
    print(i)
print("\nTHE ABOVE MENTIONED FILES WILL BE DECRYPTED\n")

choice = input("type yes to decrypt : ")
print("\n")
if choice.lower() == "yes":
    for i in files:
        print("decrypting : ", i)
        decrypt_file(key_file, i)

print("\nALL FILES ARE DECRYPTED")

if choice.lower() == "no":
    print("aborting the program, bye....")
    exit()
