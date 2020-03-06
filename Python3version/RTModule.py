import ccm
import time
import os
from datetime import datetime


class RTModule(ccm.Model):
    last_time = time.time()

    def __init__(self, file_name=None):

        if file_name == None:
            self._file_name = os.path.join(os.curdir, "rtData.csv")

        # Set up header for .csv file format
        if not os.path.exists(self._file_name):
            print("Writing new file")
            self.fh = ShallowFileHandle(self._file_name)
            self.fh.file_handle.write("agent,time_stamp,rt(seconds)\n")

        else:
            self.fh = ShallowFileHandle(self._file_name)

        self.last_time = time.time()

    def recordRT(self, *args):
        rt = (time.time() - self.last_time)

        col = "agent," + '"' + str(datetime.fromtimestamp(time.time())) + '"' + "," + str(rt)

        for x in args:
            col = col + "," + '"' + str(x) + '"'

        self.last_time = time.time()
        self.fh.file_handle.write(col + "\n")


class ShallowFileHandle():

    def __init__(self, file_name):
            self._file_name = os.path.join(os.curdir,file_name)
            self.file_handle = open(self._file_name, "a")

    def __deepcopy__(self, memo):
        return self
