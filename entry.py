__author__ = 'JordSti'
import os
import hashlib


class entry:
    (Unknown, File, Folder, Link, Root) = (-1, 0, 1, 2, 3)

    def __init__(self, name=None, parent=None, entry_type=Unknown):
        self.name = name
        self.entry_type = entry_type
        self.parent = parent
        self.childs = []

    def is_file(self):
        return self.entry_type == self.File

    def is_dir(self):
        print "CALL TO REMOVE entry.is_dir"
        return self.entry_type == self.Folder

    def is_folder(self):
        return self.entry_type == self.Folder

    def is_root(self):
        return self.entry_type == self.Root

    def is_type(self, entry_type):
        return self.entry_type == entry_type

    def add_child(self, child):
        if self.childs is not None:
            child.parent = self
            self.childs.append(child)

    def get_fullpath(self):
        fpath = self.name

        current = self.parent

        while current is not None:
            if current.is_root() and current.root_path is not None:
                fpath = os.path.join(current.root_path, fpath)
                break
            elif current.is_root():
                break
            elif not current.is_root():
                fpath = os.path.join(current.name, fpath)
                current = current.parent

        return fpath

class root_entry(entry):

    def __init__(self, root_path=None):
        entry.__init__(self, "root", None, entry.Root)
        self.root_path = root_path

class e_file(entry):

    def __init__(self, name=None, parent=None, doHash=True):
        entry.__init__(self, name, parent, self.File)
        self.childs = None
        self.__hash = None
        self.length = 0

        if os.path.exists(self.get_fullpath()) and doHash:
            self.__do_hash()

    def __do_hash(self):
        print "Hashing %s" % self.name
        buffer_size = 2048
        self.length = 0
        md5 = hashlib.md5()
        fp = open(self.get_fullpath(), 'rb')
        chunk = fp.read(buffer_size)

        while len(chunk) == buffer_size:
            md5.update(chunk)
            chunk = fp.read(buffer_size)
            self.length += len(chunk)

        md5.update(chunk)
        self.length += len(chunk)

        self.__hash = md5.hexdigest()


    def get_hash(self):
        return self.__hash

    def set_hash(self, hash):
        self.__hash = hash


class e_dir(entry):

    def __init__(self, name=None, parent=None):
        entry.__init__(self, name, parent, self.Folder)