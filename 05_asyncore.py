import asyncore


class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, 80))

        self.buffer = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'.encode()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        response = self.recv(8192)
        print(response.decode())

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


client = HTTPClient('www.python.org', '/')
asyncore.loop()
