import ccm
import time
import os
from datetime import datetime


class RTModule(ccm.Model):
    last_time = time.time()

    def __init__(self, file_name=None):

        if file_name == None:
            self._file_name = os.path.join(os.curdir, "rtData.csv")
        else:
            self._file_name = file_name

        # Set up header for .csv file format
        if not os.path.exists(self._file_name):
            print("Writing new file")
            self.fh = ShallowFileHandle(self._file_name)
            self.fh.write("agent,time_stamp,rt(seconds)\n")

        else:
            self.fh = ShallowFileHandle(self._file_name)

        self.last_time = time.time()

    def recordRT(self, *args):
        rt = (time.time() - self.last_time)

        # Create the row entry string with rt time and extra args
        entry = "agent," + '"' + str(datetime.fromtimestamp(time.time())) + '"' + "," + str(rt)
        for x in args:
            entry = entry + "," + '"' + str(x) + '"'

        self.last_time = time.time()

        # TODO: Check the return value when file is appended to
        self.fh.write(entry + "\n")


class ShallowFileHandle():

    def __init__(self, file_name):
        self._file_name = os.path.join(os.curdir,file_name)

        # TODO: Check the return value when file is opened
        self.file_handle = open(self._file_name, "a")

    def write(self, x):
        self.file_handle.write(x)
        self.file_handle.flush()

    def __deepcopy__(self, memo):
        return self
