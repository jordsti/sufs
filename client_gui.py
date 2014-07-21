__author__ = 'JordSti'
from PyQt4 import QtGui, QtCore
import gui
import sys
import network
import entry
import entry_tree
from client_request import *
from client_job import client_job

class client_gui(QtGui.QMainWindow, gui.Ui_sufs_client_form):

    def __init__(self, parent=None):
        super(client_gui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("sufs client")
        self.requests = []
        self.tree = None
        self.folder_icon = QtGui.QIcon("gui/folder.png")
        self.file_icon = QtGui.QIcon("gui/file.png")
        self.__assign_actions()
        self.__init_widgets()
        self.__init_tables()
        self.__init_tree()
        self.jobs = []
        self.selected_entries = []


    def get_endpoint(self):

        host = self.le_hostname.text()
        port = int(self.le_port.text())

        ep = network.ip_endpoint(host, port)
        return ep

    def __init_widgets(self):
        #label
        self.lbl_status_val.setText("Not connected")

    def __assign_actions(self):
        #btns
        self.btn_get_index.clicked.connect(self.launch_index_request)
        self.btn_start_job.clicked.connect(self.start_job)

        #tree
        self.tree_files.itemClicked.connect(self.tree_item_clicked)

        #menu
        self.actionQuit.triggered.connect(self.close)

    def tree_item_clicked(self, src, args):
        e = src.item

        if e.is_file():
            if src.checkState(0) == QtCore.Qt.Checked:
                if e not in self.selected_entries:
                    self.selected_entries.append(e)
                    self.lw_selected_files.addItem(e.get_fullpath())
            else:
                if e in self.selected_entries:
                    self.selected_entries.remove(e)
                    nb = self.lw_selected_files.count()
                    i = 0
                    while i < nb:
                        iw = self.lw_selected_files.item(i)
                        if str(iw.text()) == e.get_fullpath():
                            self.lw_selected_files.takeItem(i)
                            break

                        i += 1

        elif e.is_folder():
            if src.checkState(0) == QtCore.Qt.Checked:
                self.__recursive_add_item(src)
            else:
                self.__recursive_remove_item(src)

    def __recursive_remove_item(self, parent):
        nb = parent.childCount()
        for i in range(nb):
            cw = parent.child(i)
            e = cw.item
            if e.is_file():
                cw.setCheckState(0, QtCore.Qt.Unchecked)
                self.selected_entries.remove(e)
                lnb = self.lw_selected_files.count()
                li = 0
                while li < lnb:
                    wi = self.lw_selected_files.item(li)
                    if str(wi.text()) == e.get_fullpath():
                        self.lw_selected_files.takeItem(li)
                        break
                    li += 1

            elif e.is_folder():
                cw.setCheckState(0, QtCore.Qt.Unchecked)
                self.__recursive_remove_item(cw)

    def __recursive_add_item(self, parent):
        nb = parent.childCount()
        for i in range(nb):
            cw = parent.child(i)
            e = cw.item
            if e.is_file():
                cw.setCheckState(0, QtCore.Qt.Checked)
                self.lw_selected_files.addItem(e.get_fullpath())
                self.selected_entries.append(e)
            elif e.is_folder():
                cw.setCheckState(0, QtCore.Qt.Checked)
                self.__recursive_add_item(cw)

    def __init_tables(self):
        columns = QtCore.QStringList()
        columns.append("Job Id")
        columns.append("Status")
        columns.append("Progress")
        columns.append("Current file")

        self.tbl_jobs.setColumnCount(columns.count())
        self.tbl_jobs.setHorizontalHeaderLabels(columns)

    def __init_tree(self):
        columns = QtCore.QStringList()
        columns.append("Name")
        columns.append("File size")
        columns.append("File Hash (MD5)")

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
                tf.setText(1, e.get_size())
                tf.setText(2, e.get_hash())
                tf.setIcon(0, self.file_icon)
                #w_tree.addChild(tf)
                self.tree_files.addTopLevelItem(tf)
            elif e.is_folder():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                tf.setIcon(0 , self.folder_icon)
                #w_tree.addChild(tf)
                self.__fill_tree(e, tf)
                self.tree_files.addTopLevelItem(tf)
            tf.setFlags(tf.flags() | QtCore.Qt.ItemIsUserCheckable)
            tf.setCheckState(0, QtCore.Qt.Unchecked)
            tf.item = e

    def __fill_tree(self, folder_entry, tree_item):
        for e in folder_entry.childs:
            if e.is_file():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                tf.setText(1, e.get_size())
                tf.setText(2, e.get_hash())
                tf.setIcon(0, self.file_icon)
                tree_item.addChild(tf)
            elif e.is_folder():
                tf = QtGui.QTreeWidgetItem()
                tf.setText(0, e.name)
                tf.setIcon(0 , self.folder_icon)
                tree_item.addChild(tf)
                self.__fill_tree(e, tf)
            tf.setFlags(tf.flags() | QtCore.Qt.ItemIsUserCheckable)
            tf.setCheckState(0, QtCore.Qt.Unchecked)
            tf.item = e

    def job_update(self, args):
        print args.job_id, args.progress, args.current_files, args.progress

    def start_job(self):

        if len(self.selected_entries) > 0:
            print "Starting job"
            #todo handle if other jobs are running...

            job = client_job(self.get_endpoint(), self.selected_entries)
            job.job_update.connect(self.job_update)
            job.start()


            #todo add job into the table
            self.jobs.append(job)

            self.tbl_jobs.insertRow(0)

            cell = QtGui.QTableWidgetItem()
            cell.setText("%d" % job.job_id)
            self.tbl_jobs.setItem(0, 0, cell)

            cell = QtGui.QTableWidgetItem()
            cell.setText("")
            self.tbl_jobs.setItem(0, 1, cell)

            cell = QtGui.QTableWidgetItem()
            cell.setText("0 %")
            self.tbl_jobs.setItem(0, 2, cell)


    def main(self):
        self.show()

if __name__ == '__main__':
    #todo a more elegant main script
    app = QtGui.QApplication(sys.argv)
    _client_gui = client_gui()
    _client_gui.main()
    app.exec_()