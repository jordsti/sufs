__author__ = 'JordSti'
import socket


class client:

    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def endpoint(self):
        return self.host, self.port

    def send(self, data):
        self.socket.sendto(data, self.endpoint())
        print self.socket.recv(1024)


if __name__ == '__main__':

    c = client('127.0.0.1')
    c.send('josh limit')
