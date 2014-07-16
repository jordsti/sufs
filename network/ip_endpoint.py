__author__ = 'JordSti'


class ip_endpoint:

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def get_address(self):
        return self.hostname, self.port

    def from_string(self, text):
        data = text.split(':')
        if len(data) == 2:
            self.hostname = data[0]
            self.port = int(data[1])

    def to_string(self):
        return "%s:%d" % (self.hostname, self.port)