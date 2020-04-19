##############################
##### (c) E. Greve, 2019 #####
##### FOUR BUTTON PLAYER #####
### SGOMS production model ###
##############################

import sys
#sys.path.append('/Users/robertwest/CCMSuite')
sys.path.append('/Users/robertwest/pythonACTR3-master/')

import ccm
from random import randrange, uniform
from Emily import MyAgent
from Manager import Manager
log = ccm.log()
#log=ccm.log(html=True)
from ccm.lib.actr import *

class hyrule (ccm.Model):

### objects for task preformance
    response = ccm.Model(isa='response', state='state')
    display = ccm.Model(isa='diplay', state='HW')
    response_entered = ccm.Model(isa='response_entered', state='no')
    vision_finst = ccm.Model(isa='motor_finst', state='re_set')

######## run model #########
link = MyAgent()         # name the agent
zelda = Manager()        # name the Manager
env = hyrule()           # name the environment
env.agent = link         # put the agent in the environment
ccm.log_everything(env)  # print out what happens in the environment
env.run()                # run the environment
ccm.finished()           # stop the environment
