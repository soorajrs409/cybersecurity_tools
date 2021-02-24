from cryptography.fernet import Fernet

key_path = input("enter the path to store the key : ")
key1 = Fernet.generate_key()
try:
    if key_path.endswith("/"):
        #print(True)
        with open(key_path+"key1.key", "wb") as file:
            file.write(key1)
    else:
        #print(False)
        with open(key_path+"/key1.key", "wb") as file:
            file.write(key1)
    print("keys generated")
except:
    print("error occurred. please check the path ")