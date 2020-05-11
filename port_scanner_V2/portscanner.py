import socket

print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$         CREATED BY            $")
print("$          SOORAJ               $")
print("$         VERSION 1.0           $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


class PortScanner:
    banners = []
    openports = []

    def __init__(self, target, port_num):
        self.target = target
        self.port_num = port_num

    def scan(self):
        for port in range(int(self.port_num)):
            self.scan_port(port)

    def scan_port(self, port):
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((self.target, port))
            self.openports.append(port)
            try:
                banner = s.recv(1024).decode().strip("\n").strip("\r")
                self.banners.append(banner)
            except:
                self.banners.append("  ")
            s.close()
        except:
            pass
