__author__ = 'JordSti'
import SocketServer
import os
import entry
import xml.etree.ElementTree as ET
import file_instance
import network
import hashlib


class server(SocketServer.UDPServer):
    def __init__(self, port=8080, root_path='root'):
        SocketServer.UDPServer.__init__(self, ('localhost', port), connection_handler)
        self.root_path = root_path
        self.root = entry.e_dir(os.path.abspath(self.root_path))
        self.loaded_files = []
        self.index_blocks = None

        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        self.scan_root()

    def scan_root(self):
        files = os.listdir(self.root_path)
        print "Scanning root index..."
        for f in files:
            fpath = os.path.join(self.root_path, f)

            if os.path.isfile(fpath):
                e = entry.e_file(f, self.root)
                self.root.add_child(e)
            elif os.path.isdir(fpath):
                e = entry.e_dir(f)
                self.root.add_child(e)
                self.scan_folder(e)

    def scan_folder(self, folder_entry):
        folder_path = folder_entry.get_fullpath()

        files = os.listdir(folder_path)
        for f in files:
            fpath = os.path.join(folder_path, f)
            if os.path.isfile(fpath):
                e = entry.e_file(f, folder_entry)
                folder_entry.add_child(e)
            elif os.path.isdir(fpath):
                e = entry.e_dir(f)
                folder_entry.add_child(e)
                self.scan_folder(e)

    def produce_xml(self, output='index.xml'):
        print "Producing xml index"
        xml_root = ET.Element('sufs_index')
        comment = ET.Comment("File index for sufs")

        xml_root.append(comment)

        root_child = ET.SubElement(xml_root, 'root')

        for e in self.root.childs:

            if e.is_file():
                f_child = ET.SubElement(root_child, 'file', {'name': e.name, 'hash': e.get_hash()})
            elif e.is_dir():
                d_child = ET.SubElement(root_child, 'dir', {'name': e.name})
                self.xml_fill_dir(d_child, e)

        ET.ElementTree(xml_root).write(output)

    def load_xml(self):
        fe = entry.e_file('index.xml')
        fi = file_instance.file_instance(fe)
        self.index_blocks = fi
        print fi.blocks_count()


    def xml_fill_dir(self, xml_child, folder_entry):

        for c in folder_entry.childs:
            if c.is_file():
                f_child = ET.SubElement(xml_child, 'file', {'name': c.name, 'hash': c.get_hash()})
            elif c.is_dir():
                d_child = ET.SubElement(xml_child, 'dir', {'name': c.name})
                self.xml_fill_dir(d_child, c)

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


    def send_packet(self, client, packet):
        client.sendto(packet.to_chunk(), self.client_address)

if  __name__ == '__main__':

    _server = server(8080, 'C:\Users\JordSti\Downloads')
    _server.produce_xml()
    _server.load_xml()

    _server.serve_forever()
    #host, port = '127.0.0.1', 8080
    #print "starting sufs on %d" % port
    #server = SocketServer.UDPServer((host, port), connection_handler)
    #server.serve_forever()