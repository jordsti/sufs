__author__ = 'JordSti'
import block


class fc_block(block.block):
    def __init__(self, parent_hash, block_id):
        block.block.__init__(self, parent_hash, block_id)
        self.written = False
        self.data = None

    def missing(self):
        return self.data is None


class file_constructor:

    def __init__(self, name, filehash, length, blocks_size):
        self.name = name
        self.filehash = filehash
        self.length = length
        self.blocks_size = blocks_size
        self.__blocks = []
        self.__init__blocks()
        self.__completed = False

    def put_data(self, b_id, data):
        missing = False
        for b in self.__blocks:
            if b.block_id == b_id:
                if len(data) == b.length:
                    b.data = data
                    #todo handle wrong size
                elif b.missing():
                    missing = True

        if not missing:
            self.__completed = True

    def __init__blocks(self):

        b_id = 0
        for i in self.blocks_size:
            b = fc_block(self.filehash, b_id)
            b.length = i
            self.__blocks.append(b)
            b_id += 1

    def missing_blocks(self):
        """
        Returning missings blocks id
        :return:
        List of int, missings blocks id
        """
        missings = []

        for b in self.__blocks:
            if b.missing():
                missings.append(b.block_id)

        if len(missings) == 0:
            self.__completed = True

        return missings

    def is_completed(self):
        return self.__completed

    def write_to_disk(self, output):
        fp = open(output, 'wb')

        for b in self.__blocks:
            if not b.written and not b.missing():
                fp.write(b.data)
                b.written = True
                #print "%d written" % b.block_id
            else:
                fp.seek(b.length)

        fp.close()


