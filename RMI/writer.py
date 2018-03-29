import xmlrpc.client
import time
import random
import sys

class client():
    def __init__(self, server, port, access, cid):
        self.server_host = server
        self.port = int(port)
        self.access = int(access)
        self.id = int(cid)
        self.log = "Client type: Writer \nClient Name: " + str(self.id) + "\nrSeq sSeq \n\n"
        self.con = xmlrpc.client.ServerProxy('http://' + server + ':' + port, allow_none=True)

    def run(self):
        for i in range(self.access):
            rv = self.con.write(self.id)
            if rv:
                self.log += str(rv) + "   " + str(rv) + "\n"
            secs = random.randint(0, 10)
            time.sleep(secs)       
        fo = open("log" + str(self.id), "w")
        fo.write(self.log)
        fo.close()

if __name__ == '__main__':
    my_client = client(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print('writer ' + sys.argv[4])
    my_client.run()
