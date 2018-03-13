import threading
import socket
import string
import time
import random
import sys


class client():
    def __init__(self, server, port, access, cid):
        self.server_host = server
        self.port = int(port)
        self.access = int(access)
        self.id = int(cid)

    def run(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((self.server_host, self.port))
        for i in range(self.access):
            data = str(self.id)
            self.my_socket.send(data.encode())
            data = self.my_socket.recv(1024)
            if isinstance(data, bytes):
                data = data.decode()
            #print("server: " + data)
            secs = random.randint(0, 10)
            time.sleep(secs)
            self.my_socket.send('end'.encode())
            secs = random.randint(0, 10)
            time.sleep(secs)       
        self.my_socket.close()

if __name__ == '__main__':
    my_client = client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print('writer ' + sys.argv[4])
    my_client.run()
