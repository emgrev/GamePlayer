import sys
import ccm
from ccm.lib.actr import *
from random import randrange, uniform

########################
##### MOTOR MODULE #####
########################

class MotorModule(ccm.Model): # defines actions in the environment
    

##### This instantly causes changes in the environment
##### It is not a proper part of the agent    
    def referee_action(self, env_object, slot_name, slot_value):
        print('[motor module]&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        x = self.parent.parent[env_object]
        setattr(x, slot_name, slot_value)
        print (env_object)
        print(slot_name)
        print (slot_value)

##### This sees the code, which is a value in the state slot of the display object
    def see_code(self):
        self.parent.parent.vision_finst.state = 'busy' # register that the vision system is busy
        print ('[motor module] getting the code')
        #yield 0.005
        code = self.parent.parent.display.state # get the code from the state slot of the display object
        self.parent.b_visual.set(code) # put code into visual buffer
        self.parent.parent.vision_finst.state = 'see_code' # register that see_code is complete
        print ('[motor module] I see the code is..')
        print (code)

##### This enters the code
    def enter_response(self, env_object, slot_value):
        self.parent.parent.vision_finst.state = 'busy' # using vision finst for now
        yield 3
        x = eval('self.parent.parent.' + env_object)
        x.state = slot_value
        print (env_object) 
        print (slot_value)
        print ('[motor module]*******************************************************************************')
        self.parent.parent.vision_finst.state = 'enter_response' # using vision finst for now

#### This resets the finst state indicating the action is finished
#### Currently using the vision finst for all actions (so no interleaving or parallal)

    def vision_finst_reset(self):
        #yield 0.005
        self.parent.parent.vision_finst.state = 're_set' # reset the vision_finst
        print('[motor module]vision_finst_reset')
