import ccm
import time
import os
from datetime import datetime


class RTModule(ccm.Model):
    last_time = time.time()
    last_sim_time = 0

    def __init__(self, file_name=None, *args):

        if file_name == None:
            self._file_name = os.path.join(os.curdir, "rtData.csv")
        else:
            self._file_name = file_name

        # Set up header for .csv file format
        if not os.path.exists(self._file_name):
            print("Writing new file")
            self.fh = ShallowFileHandle(self._file_name)

            csv_header = "agent,time_stamp,rt(seconds),simTime_stamp,rt(sim)"

            for x in args:
                entry = entry + "," + '"' + str(x) + '"'

            self.fh.write(csv_header + '\n')

        else:
            self.fh = ShallowFileHandle(self._file_name)

        self.last_time     = time.time()
        self.flush_time    = time.time() - self.last_time

    def recordRT(self, *args):
        rt      = (time.time() - self.last_time  + self.flush_time)
        simTime = self.get_sim_time()
        rt_sim  = '%.3f'%(simTime - self.last_sim_time)

        # Create the row entry string with rt time and extra args
        entry = "agent," + '"' + str(datetime.fromtimestamp(time.time())) + '"' + "," + str(rt) + "," + str(simTime) + "," + rt_sim

        for x in args:
            entry = entry + "," + '"' + str(x) + '"'

        self.last_time = time.time()
        self.fh.write(entry + "\n")
        self.flush_time = time.time() - self.last_time
        self.last_sim_time = self.get_sim_time()

    def get_sim_time(self):
        return self.log.time._log.time


class ShallowFileHandle():

    def __init__(self, file_name):
        self._file_name = os.path.join(os.curdir,file_name)
        self.file_handle = open(self._file_name, "a")

    def write(self, x):
        self.file_handle.write(x)
        self.file_handle.flush()

        return

    def __deepcopy__(self, memo):
        return self
