import portscanner

targets_ip = input("[*] Enter the target for vuln scan : ")
port_num = int(input("[*] Enter the range of ports : "))
vuln_file = input("[*] Enter the path of the files with vulnerable softwares(txt file) : ")
print('\n')

target = portscanner.PortScanner(targets_ip, port_num)
target.scan()

with open(vuln_file, 'r') as file:
    count = 0
    for banner in target.banners:
        file.seek(0)
        for line in file.readline():
            if line.strip() in banner:
                print('[!] VULNERABLE BANNER: "' + banner + '" ON PORT:' + str(target.openports))
        count += 1
