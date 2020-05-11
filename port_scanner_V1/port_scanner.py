import socket
from time import *

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$         CREATED BY            $")
print("$          SOORAJ               $")
print("$         VERSION 1.0           $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


def scan(ip):
    print("[*] scanning ", str(ip))
    for port in range(int(port_num)):
        scan_port(ip, port)


def get_banner(s):
    return s.recv(1024)


def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(int(time_interval))
        s.connect((ip, port))
        try:
            banner = get_banner(s)
            print("[+] Open port : ", str(port), str(banner.decode()))
        except:
            print("[+] The port", str(port), "is open")
    except:
        pass
    
targets = input("[*] Enter the target/s to scan( seperate with comma) : ")
port_num = input("[*] Enter the range of ports you want to scan : ")
time_interval = input("[*] Enter the time interval for scanning each ports(in seconds) : ")

while True:
    if "," in targets:
        for ip in targets.split(","):
            scan(ip.strip(" "))
    else:
        scan(targets)
    print("Done scanning. Close the window to quit or the program will restart the scan after 10 minutes")
    sleep(600)


