import pty
from os import waitpid, execv, read, write

class SSH(object):
    def __init__(self, host, execute, user, password, askpass=True):
        self.exec_ = execute
        self.host = host
        self.user = user
        self.password = password
        self.ask_pass = askpass
        #self.run()

    def run(self):
        command = [
                '/usr/bin/ssh',
                self.user+'@'+self.host,
                '-o', 'NumberOfPasswordPrompts=1',
                self.exec_,
        ]
        pid, child_fd = pty.fork()
        if not pid:
            execv(command[0], command)

        while self.ask_pass:
            try:
                output = read(child_fd, 1024).strip()
            except Exception:
                break
            lower = output.lower()
            if b'password:' in lower:
                write(child_fd, self.password + b'\n')
                print('Logged in successfully')
                break
            elif b'are you sure you want to continue connecting' in lower:
                # Adding key to known_hosts
                write(child_fd, b'yes\n')
            else:
                print('Error:', output)

        output = []
        while True:
            try:
                output.append(read(child_fd, 1024).strip())
            except:
                break

        waitpid(pid, 0)
        output_str = [i.decode() for i in output]
        return ''.join(output_str)
