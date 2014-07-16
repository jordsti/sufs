__author__ = 'JordSti'
import socket
import network
import file_constructor

class client:

    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer_size = 4096

    def endpoint(self):
        return self.host, self.port

    def send(self, data):
        self.socket.sendto(data, self.endpoint())


    def receive(self):
        data = self.socket.recv(self.buffer_size)
        p = network.packet(data)
        return p

if __name__ == '__main__':

    c = client('127.0.0.1')
    p = network.packet()
    p.header = network.packet_header()
    p.header.packet_type = network.packet_header.Request
    p.header.fields['request'] = 'file_index'
    c.send(p.to_chunk())
    recv = c.receive()
    bcount = len(recv.header.fields['blocks'].split(','))
    bsize = []
    length = int(recv.header.fields['length'])

    for bs in recv.header.fields['blocks'].split(','):
        bsize.append(int(bs))

    print bsize

    name = recv.header.fields['name']
    fhash = recv.header.fields['hash']
    fc = file_constructor.file_constructor(name, fhash, length, bsize)
    print fc.missing_blocks()

    for i in fc.missing_blocks():
        print i
        p = network.packet()
        p.header = network.packet_header()
        p.header.packet_type = network.packet_header.Request
        p.header.fields['request'] = 'index_block'
        p.header.fields['block_id'] = str(i)
        c.send(p.to_chunk())
        recv = c.receive()
        print recv.to_string()

        if recv.header.packet_type == network.packet_header.FileBlock:
            block_id = int(recv.header.fields['block_id'])
            print "%d received" % block_id
            fc.put_data(block_id, recv.bytes)

    fc.write_to_disk(".index_cache")

    if fc.is_completed():
        print "File completed"
    #md5 summing