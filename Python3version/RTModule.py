import ccm
import time
import os
from datetime import datetime

### TODO: Need a way to add additional arguments so new features/columns can be easily added
### May be able to do this with args* in initialization and recordRT() function

class RTModule(ccm.Model):
    #clock = time.time()
    last_time = time.time()

    def __init__(self, file_name=None):

        if file_name == None:
            self._file_name = os.path.join(os.curdir, "rtData.csv")

        # Set up header for .csv file format
        if not os.path.exists(self._file_name):
            print("Writing new file")
            open(self._file_name, "w").write("agent,time_stamp,rt(seconds)\n")

        self.last_time = time.time()

    def recordRT(self, *args):
        rt = (time.time() - self.last_time)

        col = "agent," + '"' + str(datetime.fromtimestamp(time.time())) + '"' + "," + str(rt)

        for x in args:
            col = col + "," + '"' + str(x) + '"'

        self.last_time = time.time()
        f = open(self._file_name, "a")
        f.write(col + "\n")
        f.close()

#test = RTModule()
#test.recordRT()
#test.recordRT()
