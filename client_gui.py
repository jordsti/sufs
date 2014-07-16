__author__ = 'JordSti'
from PyQt4 import QtGui, QtCore
import gui
import sys
import network
import entry
import entry_tree
from client_request import *


class client_gui(QtGui.QMainWindow, gui.Ui_sufs_client_form):

    def __init__(self, parent=None):
        super(client_gui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("sufs client")
        self.requests = []
        self.tree = None
        self.__assign_actions()
        self.__init_tree()


    def get_endpoint(self):

        host = self.le_hostname.text()
        port = int(self.le_port.text())

        ep = network.ip_endpoint(host, port)
        return ep

    def __assign_actions(self):

        self.btn_get_index.clicked.connect(self.launch_index_request)
        self.lbl_status_val.setText("Not connected")

    def __init_tree(self):
        columns = QtCore.QStringList()
        columns.append("Name")
        columns.append("Nothing")

        self.tree_files.setColumnCount(columns.count())
        self.tree_files.setHeaderLabels(columns)

    def launch_index_request(self):
        index_req = index_request(self.get_endpoint(), self.index_request_completed)
        self.requests.append(index_req)
        self.lbl_status_val.setText("Asking server index...")
        index_req.start()

    def index_request_completed(self, request):
        #todo pending support
        print "request completed"
        #self.requests.remove(request)
        print "retrieving index blocks"
        self.lbl_status_val.setText("Receiving index")
        blocks_req = index_retrieve(self.get_endpoint(), request.index_ctor, self.index_blocks_downloaded)
        self.requests.append(blocks_req)
        blocks_req.start()

    def index_blocks_downloaded(self, request):
        request.index_ctor.write_to_disk('.sufs_index.cache')
        self.lbl_status_val.setText("Index received!")

        #load this into grid
        print "loading root"
        self.load_index_root()

    def load_index_root(self):
        self.tree = entry_tree.entry_tree()
        self.tree.from_xml('.sufs_index.cache')

        #w_tree = QtGui.QTreeWidgetItem()

        for e in self.tree.root.childs:

            if e.is_file():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                #w_tree.addChild(tf)
                self.tree_files.addTopLevelItem(tf)
            elif e.is_folder():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                #w_tree.addChild(tf)
                self.__fill_tree(e, tf)
                self.tree_files.addTopLevelItem(tf)

    def __fill_tree(self, folder_entry, tree_item):
        for e in folder_entry.childs:
            if e.is_file():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                tree_item.addChild(tf)
            elif e.is_folder():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                tree_item.addChild(tf)
                self.__fill_tree(e, tf)


    def main(self):
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    _client_gui = client_gui()
    _client_gui.main()
    app.exec_()