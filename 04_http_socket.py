import socket


def http_get(host, path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))

    buffer = f'GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n'.encode()

    while len(buffer) > 0:
        sent = sock.send(buffer)
        buffer = buffer[sent:]

    response = sock.recv(8192)
    print(response.decode())


http_get('www.python.org', '/')
