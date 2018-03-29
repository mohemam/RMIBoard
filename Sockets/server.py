import socket
import threading
import time
import subprocess
import sys

class server():
        def __init__(self, address, port, n_readers, n_writers, access):
            self.address = address
            self.port = int(port)
            self.n_clients = int(n_readers) + int(n_writers)
            self.n_access = int(access)
            self.oval = -1
            self.sseq = 0
            self.r_ids = []
            self.w_id = -1
            self.rnum = 0
            self.read_log = "Readers: \n\nsSeq oVal rID rNum \n\n"
            self.write_log = "Writers: \n\nsSeq oVal wID \n\n"
            self.mutex = threading.Lock()
            self.seqmutex = threading.Lock()

        # Start running the server
        def run(self):
            # Create server socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind the Socket to a puclic host
            self.socket.bind((self.address, self.port))
            # Max Number of connections allowed is 1
            self.socket.listen(self.n_clients)
            for i in range(self.n_clients):
                # Accepting connection from client
                client_socket, client_addr = self.socket.accept()
                #client_socket.settimeout(60)
                # Receiving Messages from client on separate thread
                threading.Thread(target=self.receive, args = (client_socket, client_addr)).start()
            time.sleep(60)
            fo = open("log", "w")
            fo.write(self.read_log + "\n\n" + self.write_log)
            fo.close()

        # Receive Messages from client
        def receive(self, client, address):
            is_r = True
            cid = -1
            seq = -1
            for i in range(self.n_access):
                data = client.recv(1024)
                with self.seqmutex:
                    self.sseq += 1
                    seq = self.sseq
                if isinstance(data, bytes):
                    data = data.decode()
                if data.startswith('r'):
                    is_r = True
                    dl = data.split(' ')
                    if dl[1] not in self.r_ids: 
                        self.r_ids.append(dl[1])
                        cid = dl[1]
                    client.send((str(self.oval) + ' ' + str(seq)).encode())
                else:
                    is_r = False
                    with self.mutex:
                        self.oval = int(data)
                    cid = int(data)
                    #print("client: " + data)
                    client.send(str(seq).encode())
                if is_r:
                    self.read_log += str(seq) + "    " + str(self.oval) + "    " + str(cid) + "     " + str(len(self.r_ids)) + "\n"
                    #print(self.read_log)
                    #self.r_ids.remove(cid)
                else:
                    self.write_log += str(seq) + "    " + str(self.oval) + "     " + str(cid) + "\n"
                response = client.recv(1024)
                while response.decode() != 'end':
                    print(response)
                    response = client.recv(1024)
                if is_r:
                    self.r_ids.remove(cid)

        # Ending Chat
        def kill(self):
            # Close chat socket
            self.client_socket.close()

if __name__ == '__main__':
    print('Server started')
    my_server = server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    my_server.run()
