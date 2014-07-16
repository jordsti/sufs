__author__ = 'JordSti'
import os
import entry
import xml.etree.ElementTree as ET

def get_indent_str(indent):
    txt = ''
    for i in range(indent):
        txt += '\t'
    return txt

class entry_tree:

    def __init__(self, root_path=None):
        self.root = None
        self.root_path = root_path

        if self.root_path is not None:
            pass
        #scanroot

    def print_tree(self):
        txt = ""
        txt += "Printing Tree\n"
        txt += "[root]\n"
        for c in self.root.childs:
            if c.is_file():
                txt += "-%s  hash: %s length: %d\n" % (c.name, c.get_hash(), c.length)
            elif c.is_dir():
                txt += self.__print_folder(c)

        print txt

    def __print_folder(self, folder, indent=1):
        txt = ""
        txt += "%s[%s]\n" % (get_indent_str(indent), folder.name)

        for c in folder.childs:
            if c.is_file():
                txt += "%s-%s  hash: %s length: %d fp: %s\n" % (get_indent_str(indent),c.name, c.get_hash(), c.length, c.get_fullpath())
            elif c.is_dir():
                txt += self.__print_folder(c, indent + 1)

        return txt


    def build_tree(self, root_path):
        self.root_path = root_path
        files = os.listdir(self.root_path)
        self.root = entry.root_entry(root_path)
        print "Scanning root index..."
        for f in files:
            #print f
            if not f.startswith('.'):
                fpath = os.path.join(self.root_path, f)
                if os.path.isfile(fpath):
                    e = entry.e_file(f, self.root)
                    self.root.add_child(e)
                elif os.path.isdir(fpath):
                    e = entry.e_dir(f)
                    self.root.add_child(e)
                    self.__scan_folder(e)

    def __scan_folder(self, folder_entry):
        folder_path = folder_entry.get_fullpath()
        files = os.listdir(folder_path)
        for f in files:
            #print f
            if not f.startswith('.'):
                fpath = os.path.join(folder_path, f)
                if os.path.isfile(fpath):
                    e = entry.e_file(f, folder_entry)
                    folder_entry.add_child(e)
                elif os.path.isdir(fpath):
                    e = entry.e_dir(f)
                    folder_entry.add_child(e)
                    self.__scan_folder(e)

    def from_xml(self, input):
        xml_tree = ET.parse(input)

        xml_root = xml_tree.getroot()

        if xml_root.tag == 'sufs_index': # todo put this into a constants
            for child in xml_root:
                if child.tag == 'root':
                    self.root = entry.root_entry()
                for ic in child:
                    if ic.tag == 'file':
                        ef = entry.e_file(ic.attrib['name'], self.root, False)
                        ef.set_hash(ic.attrib['hash'])
                        ef.length = int(ic.attrib['length'])
                        self.root.add_child(ef)
                    elif ic.tag == 'folder':
                        ed = entry.e_dir(ic.attrib['name'], self.root)
                        self.root.add_child(ed)
                        self.__parse_xml_folder(ic, ed)



    def __parse_xml_folder(self, xml_child, folder_entry):
        for child in xml_child:
            if child.tag == 'file':
                ef = entry.e_file(child.attrib['name'], folder_entry, False)
                ef.set_hash(child.attrib['hash'])
                ef.length = int(child.attrib['length'])
                folder_entry.add_child(ef)
            elif child.tag == 'folder':
                ed = entry.e_dir(child.attrib['name'], folder_entry)
                folder_entry.add_child(ed)
                self.__parse_xml_folder(child, ed)

    def produce_xml(self, output='index.xml'):
        print "Producing xml index"
        xml_root = ET.Element('sufs_index')
        comment = ET.Comment("File index for sufs")

        xml_root.append(comment)

        root_child = ET.SubElement(xml_root, 'root')

        for e in self.root.childs:

            if e.is_file():
                f_child = ET.SubElement(root_child, 'file', {'name': e.name, 'hash': e.get_hash(), 'length': str(e.length)})
            elif e.is_dir():
                d_child = ET.SubElement(root_child, 'folder', {'name': e.name})
                self.xml_fill_dir(d_child, e)

        ET.ElementTree(xml_root).write(output)


    def xml_fill_dir(self, xml_child, folder_entry):

        for c in folder_entry.childs:
            if c.is_file():
                f_child = ET.SubElement(xml_child, 'file', {'name': c.name, 'hash': c.get_hash(), 'length': str(c.length)})
            elif c.is_dir():
                d_child = ET.SubElement(xml_child, 'folder', {'name': c.name})
                self.xml_fill_dir(d_child, c)

if __name__ == '__main__':
    print "Entry Tree Test"

    et = entry_tree()
    #et.build_tree('C:\Users\JordSti\gitprojects\dc-deck')
    et.from_xml('dc-deck.xml')
    et.print_tree()
    #et.produce_xml('dc-deck.xml')