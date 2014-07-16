__author__ = 'JordSti'
import hashlib
import network

class file_block:

    def __init__(self, parent_hash, block_id, data):
        self.parent_hash = parent_hash
        self.block_id = block_id
        self.data = data
        self.length = len(data)


class file_instance:

    (DefaultBlockSize) = 1024

    def __init__(self, file_entry, block_size = DefaultBlockSize):
        self.entry = file_entry
        self.block_size = block_size
        self.__blocks = []
        self.length = 0
        self.hash = self.entry.get_hash() #todo need to verify that hash maybe. ?
        self.__load_blocks()

    def generate_file_info_packet(self):

        p = network.packet()
        p.header = network.packet_header()
        p.header.packet_type = network.packet_header.FileInformation
        p.header.fields['hash'] = self.hash
        p.header.fields['length'] = self.length

        b_str = ""
        for b in self.each_blocks_length():
            b_str += "%d," % b
        b_str = b_str.rstrip(',')

        p.header.fields['blocks'] = b_str

        return p

    def blocks_count(self):
        return len(self.__blocks)

    def each_blocks_length(self):
        lengths = []
        for b in self.__blocks:
            lengths.append(b.length)
        return lengths

    def get_block(self, b_i):
        return self.__blocks[b_i]

    def get_block_packet(self, b_i):
        b = self.__blocks[b_i]
        p = network.packet()
        p.header = network.packet_header()
        p.header.packet_type = network.packet_header.FileBlock
        p.header.length = b.length
        p.header.fields['block_id'] = b.block_id
        p.bytes = b.data

        return p

    def __load_blocks(self):

        fp = open(self.entry.get_fullpath(), 'rb')

        chunk = fp.read(self.block_size)
        self.length = 0
        b_i = 0

        while len(chunk) == self.block_size:

            self.length += self.block_size

            block = file_block(self.hash, b_i, chunk)
            self.__blocks.append(block)

            chunk = fp.read(self.block_size)
            b_i += 1

        if len(chunk) > 0:
            block = file_block(self.hash, b_i, chunk)
            self.length += len(chunk)
            self.__blocks.append(block)

        fp.close()
