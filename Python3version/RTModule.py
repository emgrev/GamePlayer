import time
import ccm
import os
from ccm.lib.actr import *
from datetime import datetime

### TODO: Need a way to add additional arguments so new features/columns can be easily added
### May be able to do this with args* in initialization and recordRT() function

class RTModule(ccm.Model):
    #clock = time.time()
    last_time = None

    def __init__(self, file_name=None):

        if file_name == None:
            self._file_name = os.path.join(os.curdir, "rtData.csv")

        # Set up header for .csv file format
        if not os.path.exists(self._file_name):
            print("Writing new file")
            self._file_handle = open(self._file_name, "w")
            self._file_handle.write("agent,time_stamp,rt(ns)\n")
        else:
            self._file_handle = open(self._file_name, "a")

        self.last_time = time.time_ns()

    def recordRT(self):
        rt = (time.time_ns() - self.last_time) # Divide by 1000000 to convert into seconds

        col = "agent," + '"' + str(datetime.fromtimestamp(time.time())) + '"' + "," + str(rt)
        print(col)

        self.last_time = time.time_ns()
        self._file_handle.write(col + "\n")

test = RTModule()
test.recordRT()
test.recordRT()
