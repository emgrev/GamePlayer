import time
import ccm
from ccm.lib.actr import *

class RTModule(ccm.Model):
    #clock = time.time()
    last_time = None

    def __init__(file_name=None):
        this.last_time = time.time_ns()

        if file_name == None:
            this._file_name = "rt.time"

        this._file_handle = file(this._file_name, "w")

        # Set up header for .csv file format
        this._file_handle.write("")

    def recordRT():
        rt = (time.time_ns() - this.last_time)/1000000 # Divide by 1000000 to convert into seconds

        this._file_handle.write(str(rt) + ",")
