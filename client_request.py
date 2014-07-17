__author__ = 'JordSti'
from PyQt4 import QtGui, QtCore
import client
import network
import time
import file_constructor

class network_request(QtCore.QThread):

    def __init__(self, endpoint, received=None):
        QtCore.QThread.__init__(self)
        self.endpoint = endpoint
        self.received = received
        self.sent_packet = None
        self.receipt_packet = None
        self.sended_packets = []
        self.received_packets = []
        self.client = None

    def __sent_packet(self, packet):
        self.sended_packets.append(packet)
        if self.sent_packet is not None:
            self.sent_packet(self, packet)

    def __receipt_packet(self, packet):
        self.received_packets.append(packet)
        if self.receipt_packet is not None:
            self.receipt_packet(self, packet)

    def run(self):
        pass

    def recv(self):
        self.__verify_client()
        data = self.client.receive()
        recv_packet = network.packet(data)
        self.__receipt_packet(recv_packet)
        return recv_packet

    def send(self, packet):
        self.__verify_client()
        self.client.send(packet.to_chunk())
        self.__sent_packet(packet)

    def __verify_client(self):
        if self.client is None:
            self.client = client.client(self.endpoint.hostname, self.endpoint.port)
        else:
            self.client.set_endpoint(self.endpoint)

    def terminate(self):
        self.__received()

    def __received(self):

        if self.received is not None:
            self.received(self)

class index_request(network_request):

    def __init__(self, endpoint, received=None):
        network_request.__init__(self, endpoint, received)
        self.index_ctor = None

    def run(self):
        #forging packet
        p = network.packet()
        p.header = network.packet_header()
        p.header.packet_type = network.packet_header.Request
        p.header.fields['request'] = 'file_index'

        self.send(p)

        recv_packet = self.recv()

        if recv_packet.header.packet_type == network.packet_header.FileInformation:
            #index info
            bsize = []
            length = int(recv_packet.header.fields['length'])

            for bs in recv_packet.header.fields['blocks'].split(','):
                bsize.append(int(bs))

            name = recv_packet.header.fields['name']
            fhash = recv_packet.header.fields['hash']

            self.index_ctor = file_constructor.file_constructor(name, fhash, length, bsize)

        self.terminate()


class index_retrieve(network_request):

    def __init__(self, endpoint, index_ctor, received=None):
        network_request.__init__(self, endpoint, received)
        self.index_ctor = index_ctor

    def run(self):

        for m in self.index_ctor.missing_blocks():
            p = network.packet()
            p.header = network.packet_header()
            p.header.packet_type = network.packet_header.Request
            p.header.fields['request'] = 'index_block'
            p.header.fields['block_id'] = str(m)

            self.send(p)

            recv = self.recv()

            if recv.header.packet_type == network.packet_header.FileBlock:
                b_id = int(recv.header.fields['block_id'])
                self.index_ctor.put_data(b_id, recv.bytes)

        if self.index_ctor.is_completed():
            self.terminate()
        else:
            print self.index_ctor.missing_blocks()



class file_request(network_request):

    def __init__(self, endpoint, filepath, received=None):
        network_request.__init__(self, endpoint, received)
        self.file_ctor = None
        self.filepath = filepath

    def run(self):
        #forging packet
        p = network.packet()
        p.header = network.packet_header()
        p.header.packet_type = network.packet_header.Request
        p.header.fields['request'] = 'ask_file_info'
        p.header.fields['file'] = self.filepath
        self.send(p)

        recv_packet = self.recv()

        if recv_packet.header.packet_type == network.packet_header.FileInformation:
            #index info
            bsize = []
            length = int(recv_packet.header.fields['length'])

            for bs in recv_packet.header.fields['blocks'].split(','):
                bsize.append(int(bs))

            name = recv_packet.header.fields['name']
            fhash = recv_packet.header.fields['hash']

            self.file_ctor = file_constructor.file_constructor(name, fhash, length, bsize)

        self.terminate()