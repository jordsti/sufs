__author__ = 'JordSti'
import os


class entry:
    (File, Folder, Link, Unknown) = (0, 1, 2, -1)

    def __init__(self, name=None, parent=None, entry_type=Unknown):
        self.name = name
        self.entry_type = entry_type
        self.parent = parent
        self.childs = []

    def is_file(self):
        return self.entry_type == self.File

    def is_dir(self):
        return self.entry_type == self.Folder

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
            fpath = os.path.join(current.name, fpath)
            current = current.parent

        return fpath



class e_file(entry):

    def __init__(self, name=None, parent=None):
        entry.__init__(self, name, parent, self.File)
        self.childs = None


class e_dir(entry):

    def __init__(self, name=None, parent=None):
        entry.__init__(self, name, parent, self.Folder)