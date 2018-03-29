import socket
import threading
import time
import subprocess
import sys
import random
from xmlrpc.server import SimpleXMLRPCServer

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
            self.rlogmutex = threading.Lock()
            self.wlogmutex = threading.Lock()

        # Start running the server
        def run(self):
            threading.Thread(target=self.check_server).start()
            #with SimpleXMLRPCServer((self.address, self.port)) as self.server:
            self.server = SimpleXMLRPCServer((self.address, self.port))
            self.sock = self.server.socket
            self.server.register_introspection_functions()
            self.server.register_function(self.read)
            self.server.register_function(self.write)
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                exit(0)
            fo = open("log", "w")
            fo.write(self.read_log + "\n\n" + self.write_log)
            fo.close()

        def stop_server(self):
            self.server.shutdown()
            self.server.server_close()

        def check_server(self):
            while self.n_clients > self.sseq + 1:
                pass
            time.sleep(180)
            self.stop_server()

        def read(self, rid):
            seq = -1
            with self.seqmutex:
                self.sseq += 1
                seq = self.sseq
            if rid not in self.r_ids:
                self.r_ids.append(rid)
            secs = random.randint(0, 10)
            time.sleep(secs)
            with self.rlogmutex:
                self.read_log += str(seq) + "    " + str(self.oval) + "    " + str(rid) + "     " + str(len(self.r_ids)) + "\n"
            self.r_ids.remove(rid)
            return self.oval, seq

        def write(self, wid):
            seq = -1
            with self.seqmutex:
                self.sseq += 1
                seq = self.sseq
            with self.mutex:
                self.oval = wid
            secs = random.randint(0, 10)
            time.sleep(secs)
            with self.wlogmutex:
                self.write_log += str(seq) + "    " + str(self.oval) + "     " + str(wid) + "\n"
            return seq

if __name__ == '__main__':
    print('Server started')
    my_server = server(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    my_server.run()
