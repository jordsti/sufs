# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'client_form.ui'
#
# Created: Mon Jul 21 17:10:53 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_sufs_client_form(object):
    def setupUi(self, sufs_client_form):
        sufs_client_form.setObjectName(_fromUtf8("sufs_client_form"))
        sufs_client_form.resize(761, 588)
        self.centralwidget = QtGui.QWidget(sufs_client_form)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gb_server_info = QtGui.QGroupBox(self.centralwidget)
        self.gb_server_info.setGeometry(QtCore.QRect(10, 10, 231, 121))
        self.gb_server_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gb_server_info.setObjectName(_fromUtf8("gb_server_info"))
        self.formLayoutWidget = QtGui.QWidget(self.gb_server_info)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 20, 221, 71))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.gp_srv_info_layout = QtGui.QFormLayout(self.formLayoutWidget)
        self.gp_srv_info_layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.gp_srv_info_layout.setMargin(0)
        self.gp_srv_info_layout.setObjectName(_fromUtf8("gp_srv_info_layout"))
        self.lblHostname = QtGui.QLabel(self.formLayoutWidget)
        self.lblHostname.setObjectName(_fromUtf8("lblHostname"))
        self.gp_srv_info_layout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblHostname)
        self.le_hostname = QtGui.QLineEdit(self.formLayoutWidget)
        self.le_hostname.setObjectName(_fromUtf8("le_hostname"))
        self.gp_srv_info_layout.setWidget(0, QtGui.QFormLayout.FieldRole, self.le_hostname)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gp_srv_info_layout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.le_port = QtGui.QLineEdit(self.formLayoutWidget)
        self.le_port.setObjectName(_fromUtf8("le_port"))
        self.gp_srv_info_layout.setWidget(1, QtGui.QFormLayout.FieldRole, self.le_port)
        self.lbl_status = QtGui.QLabel(self.formLayoutWidget)
        self.lbl_status.setObjectName(_fromUtf8("lbl_status"))
        self.gp_srv_info_layout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_status)
        self.lbl_status_val = QtGui.QLabel(self.formLayoutWidget)
        self.lbl_status_val.setObjectName(_fromUtf8("lbl_status_val"))
        self.gp_srv_info_layout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lbl_status_val)
        self.btn_get_index = QtGui.QPushButton(self.gb_server_info)
        self.btn_get_index.setGeometry(QtCore.QRect(120, 90, 101, 23))
        self.btn_get_index.setObjectName(_fromUtf8("btn_get_index"))
        self.tree_files = QtGui.QTreeWidget(self.centralwidget)
        self.tree_files.setGeometry(QtCore.QRect(10, 140, 611, 271))
        self.tree_files.setObjectName(_fromUtf8("tree_files"))
        self.tree_files.headerItem().setText(0, _fromUtf8("1"))
        self.gb_job = QtGui.QGroupBox(self.centralwidget)
        self.gb_job.setGeometry(QtCore.QRect(250, 10, 371, 121))
        self.gb_job.setObjectName(_fromUtf8("gb_job"))
        self.lw_selected_files = QtGui.QListWidget(self.gb_job)
        self.lw_selected_files.setGeometry(QtCore.QRect(10, 20, 271, 91))
        self.lw_selected_files.setObjectName(_fromUtf8("lw_selected_files"))
        self.btn_start_job = QtGui.QPushButton(self.gb_job)
        self.btn_start_job.setGeometry(QtCore.QRect(290, 20, 75, 23))
        self.btn_start_job.setObjectName(_fromUtf8("btn_start_job"))
        self.tbl_jobs = QtGui.QTableWidget(self.centralwidget)
        self.tbl_jobs.setGeometry(QtCore.QRect(10, 420, 611, 111))
        self.tbl_jobs.setObjectName(_fromUtf8("tbl_jobs"))
        self.tbl_jobs.setColumnCount(0)
        self.tbl_jobs.setRowCount(0)
        sufs_client_form.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(sufs_client_form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        sufs_client_form.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(sufs_client_form)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        sufs_client_form.setStatusBar(self.statusbar)
        self.actionConnect_to_a_server = QtGui.QAction(sufs_client_form)
        self.actionConnect_to_a_server.setObjectName(_fromUtf8("actionConnect_to_a_server"))
        self.actionQuit = QtGui.QAction(sufs_client_form)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menu_File.addAction(self.actionConnect_to_a_server)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())

        self.retranslateUi(sufs_client_form)
        QtCore.QMetaObject.connectSlotsByName(sufs_client_form)

    def retranslateUi(self, sufs_client_form):
        sufs_client_form.setWindowTitle(_translate("sufs_client_form", "MainWindow", None))
        self.gb_server_info.setTitle(_translate("sufs_client_form", "Server Information", None))
        self.lblHostname.setText(_translate("sufs_client_form", "Hostname :", None))
        self.le_hostname.setText(_translate("sufs_client_form", "127.0.0.1", None))
        self.label_2.setText(_translate("sufs_client_form", "Port :", None))
        self.le_port.setText(_translate("sufs_client_form", "8080", None))
        self.lbl_status.setText(_translate("sufs_client_form", "Status :", None))
        self.lbl_status_val.setText(_translate("sufs_client_form", "lbl_status_val", None))
        self.btn_get_index.setText(_translate("sufs_client_form", "Retrieve Index", None))
        self.gb_job.setTitle(_translate("sufs_client_form", "Selected file(s)", None))
        self.btn_start_job.setText(_translate("sufs_client_form", "Start Job", None))
        self.menu_File.setTitle(_translate("sufs_client_form", "&File", None))
        self.actionConnect_to_a_server.setText(_translate("sufs_client_form", "Connect to a server...", None))
        self.actionQuit.setText(_translate("sufs_client_form", "Quit", None))

