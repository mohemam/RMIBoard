import socket
import threading
import time
import subprocess
import shlex
import ssh

class system():
        def __init__(self):
            fo = open("config.txt")
            configs = fo.read()
            fo.close()
            lines = []
            lines = configs.split('\n')
            self.properties = {}
            for l in lines:
                props = []
                #print(l)
                if l == "":
                    continue
                props = l.split('RW.')
                #print(props)
                for p in props:
                    #print(p)
                    if p == "":
                        continue
                    pk = p.split('=')
                    self.properties[pk[0].strip()] = pk[1].strip()
            #print(self.properties)
            self.password = ""
            self.user = 'emam'

        def start(self):
            for i in range(int(self.properties['numberOfReaders'])):
                threading.Thread(target=self.run_readers, args = (i,)).start()
            for i in range(int(self.properties['numberOfWriters'])):
                threading.Thread(target=self.run_writers, args = (i+int(self.properties['numberOfReaders']),)).start()
            #command = "sshpass -p " + self.password + "ssh " + self.user + "@" + self.properties['server'] + " "
            #command = "ssh " + self.user + "@" + self.properties['server'] + " "
            command = "python3 server.py " + self.properties['server'] + " " + self.properties['server.port'] + " " + self.properties['numberOfReaders'] + " " + self.properties['numberOfWriters'] + " " + self.properties['numberOfAccesses']
            #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            #output, error = process.communicate()
            #args = shlex.split(command)
            #process = subprocess.Popen(args)
            #output, error = process.communicate()
            myssh = ssh.SSH(self.properties['server'] , execute=command, askpass=True, user=self.user, password=self.password.encode())
            myssh.run()

        def run_readers(self, i):
            time.sleep(0.5)
            command = "python3 reader.py " + self.properties['server'] + " " + self.properties['server.port'] + " " + self.properties['numberOfAccesses'] + " " + str(i)
            args = shlex.split(command)
            process = subprocess.Popen(args)
            output, error = process.communicate()

        def run_writers(self, i):
            time.sleep(0.5)
            command = "python3 writer.py " + self.properties['server'] + " " + self.properties['server.port'] + " " + self.properties['numberOfAccesses'] + " " + str(i)
            args = shlex.split(command)
            process = subprocess.Popen(args)
            output, error = process.communicate()

if __name__ == '__main__':
    my_system = system()
    my_system.start()
