__author__ = 'JordSti'
import os
from PyQt4 import QtCore
import time
import client_request


current_job_id = 0

def get_job_id():
    global current_job_id
    job_id = current_job_id
    current_job_id += 1
    return job_id


class job_update_args:

    (Pending, WaitingForFileInfo, DownloadingFile, Completed) = (0, 1, 2, 3)

    def __init__(self, src, status=Pending, progress=0, current_files=""):
        self.src = src
        self.job_id = src.job_id
        self.progress = progress
        self.current_files = current_files
        self.status = status


class client_job(QtCore.QThread):
    (job_update) = QtCore.pyqtSignal(object)

    def __init__(self, endpoint, selected_entries=[], reception_folder='recv'):
        QtCore.QThread.__init__(self)
        self.endpoint = endpoint
        self.selected_entries = selected_entries
        self.completed_entries = []
        self.reception_folder = reception_folder
        self.file_ctor = None
        self.__init_folder()
        self.job_id = get_job_id()
        self.total_length = 0.00
        self.current_length = 0.00

        self.__sum_length()

    def __sum_length(self):
        self.total_length = 0
        for e in self.selected_entries:
            self.total_length += float(e.length)

    def __init_folder(self):
        if not os.path.exists(self.reception_folder):
            os.makedirs(self.reception_folder)

    def __retrieve_file(self, file_entry):
        #todo emit update data
        local_path = os.path.join(self.reception_folder, file_entry.get_fullpath())
        print local_path
        if os.path.exists(local_path):
            print "Error [File Exists Already !] - %s" % local_path
            #todo manage this, like do a file hash and if hash is not matching download the file
            return

        #retrieve file info

        request = client_request.file_request(self.endpoint, file_entry.get_fullpath())

        args = job_update_args(self, job_update_args.WaitingForFileInfo, (self.current_length / self.total_length) * 100, file_entry.get_fullpath(), )
        self.job_update.emit(args)

        request.start()

        while not request.completed:
            print "Waiting on file info..."
            print str(request.completed)
            time.sleep(0.5)

        self.file_ctor = request.file_ctor
        #requesting blocks

        request = client_request.file_retrieve(self.endpoint, self.file_ctor)

        args = job_update_args(self, job_update_args.DownloadingFile, (self.current_length / self.total_length) * 100.00, file_entry.get_fullpath())
        self.job_update.emit(args)

        request.start()

        while not request.completed:
            print "waiting on file retrieve.."
            time.sleep(0.5)

        parent_folder = os.path.dirname(local_path)
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)

        self.file_ctor.write_to_disk(local_path)

        #todo more accurate current length needed
        self.current_length += float(self.file_ctor.length)

    def run(self):
        args = job_update_args(self)
        self.job_update.emit(args)
        for entry in self.selected_entries:
            if entry.is_file():
                #todo retrieve file
                self.__retrieve_file(entry)

        args = job_update_args(self, job_update_args.Completed, 100)
        self.job_update.emit(args)

