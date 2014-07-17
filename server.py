__author__ = 'JordSti'
import SocketServer
import os
import entry
import xml.etree.ElementTree as ET
import file_instance
import network
import entry_tree
import hashlib


class server(SocketServer.UDPServer):
    def __init__(self, port=8080, root_path='root'):
        SocketServer.UDPServer.__init__(self, ('localhost', port), connection_handler)
        self.root_path = root_path
        #self.root = entry.e_dir(os.path.abspath(self.root_path))
        self.root = entry_tree.entry_tree()
        self.loaded_files = []
        self.index_blocks = None

        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)

    def scan_root(self):
        self.root.build_tree(self.root_path)
        self.root.produce_xml('index.xml')
        self.load_xml()


    def load_xml(self):
        fe = entry.e_file('index.xml')
        fi = file_instance.file_instance(fe)
        self.index_blocks = fi
        print "Blocks Count : %d" % fi.blocks_count()

    def get_file(self, hash):
        for fi in self.loaded_files:
            if fi.hash == hash:
                return fi

        return None

class connection_handler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        client = self.request[1]
        print self.server.root_path

        print "Received: %s" % data
        print "From: %s:%d" % (self.client_address[0], self.client_address[1])
        recv_packet = network.packet(data)

        if recv_packet.header.packet_type == network.packet_header.Request:
            req = recv_packet.header.fields['request']
            if req == 'file_index':
                #sending block info
                file_info = self.server.index_blocks.generate_file_info_packet()
                self.send_packet(client, file_info)
            elif req == 'index_block':
                b_id = int(recv_packet.header.fields['block_id'])
                if b_id < self.server.index_blocks.blocks_count():
                    block_packet = self.server.index_blocks.get_block_packet(b_id)
                    self.send_packet(client, block_packet)
            elif req == 'ask_file_info':
                rel_path = recv_packet.header.fields['file']
                fe = self.server.get_entry(rel_path)
                if fe is not None:
                    #load this file info memory
                    fi = file_instance.file_instance(fe)
                    self.server.loaded_files.append(fi)
                    info_packet = fi.generate_file_info_packet()
                    self.send_packet(info_packet)
            elif req == 'file_block':
                b_id = int(recv_packet.header.fields['block_id'])
                file_hash = recv_packet.header.fields['hash']
                fi = self.server.get_file(file_hash)
                if fi is not None:
                    bp = fi.get_block_packet(b_id)
                    self.send_packet(bp)



    def send_packet(self, client, packet):
        client.sendto(packet.to_chunk(), self.client_address)

if  __name__ == '__main__':

    _server = server(8080, '../pydbg')

    _server.scan_root()

    #_server.serve_forever()
    #host, port = '127.0.0.1', 8080
    #print "starting sufs on %d" % port
    _server.serve_forever()