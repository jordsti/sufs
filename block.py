__author__ = 'JordSti'


class block:
    def __init__(self, parent_hash, block_id):
        self.parent_hash = parent_hash
        self.block_id = block_id
        self.data = None
        self.length = 0