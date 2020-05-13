import hashlib
import os

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$    HASH-CRACKER CREATED BY    $")
print("$           SOORAJ              $")
print("$         VERSION 1.0           $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print('\n')

hash_type = str(input("[*] Enter the type to hash you want to crack : "))
password_file = str(input("[*] Enter the path of password file (txt format) : "))
hash = str(input("[*] Enter the hash that you want to crack : "))

if not os.path.exists(password_file):
    print("\n[-] Password file not found")
else:
    with open(password_file, 'r') as file:
        for line in file.readlines():
            if hash_type == "md5":
                hash_object = hashlib.md5(line.strip().encode())
                hashed_word = hash_object.hexdigest()
                if hashed_word == hash:
                    print("[+] MD5 Password found : ", line.strip())
                    exit(0)
            if hash_type == "sha1":
                hash_object = hashlib.sha1(line.strip().encode())
                hashed_word = hash_object.hexdigest()
                if hashed_word == hash:
                    print("[+] SHA1 Passowrd found : ", line.strip())
                    exit(0)

        print("[!] Password Not Found In The File( Try With different password file ) ")


