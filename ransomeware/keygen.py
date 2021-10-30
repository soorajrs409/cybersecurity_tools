from cryptography.fernet import Fernet

keyPath = "/"


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


genKey(keyPath)

