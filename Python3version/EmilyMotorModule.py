import sys
import ccm
from ccm.lib.actr import *
from random import randrange, uniform

########################
##### MOTOR MODULE #####
########################

class EmilyMotorModule(ccm.Model): # defines actions in the environment
    

##### This instantly causes changes in the environment
##### It is not a proper part of the agent    
    def referee_action(self, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        setattr(x, slot_name, slot_value)
        print('[referee]')
        print('object=',env_object)
        print('slot=',slot_name)
        print('value=',slot_value)

##### This sees the code, which is a value in the state slot of the display object
    def see_code(self):
        self.parent.parent.vision_finst.state = 'busy' # register that the vision system is busy
        #yield 4
        print ('[vision - looking]')
        code = self.parent.parent.display.state # get the code from the state slot of the display object
        self.parent.b_visual.set(code) # put code into visual buffer
        self.parent.b_method.set('state:finished')
        print ('[vision - I see the code is..',code,']')
        self.parent.parent.vision_finst.state = 'finished'

##### This enters the code
    def enter_response(self, env_object, slot_value):
        self.parent.parent.vision_finst.state = 'busy'
        #yield 3
##        x = eval('self.parent.parent.' + env_object)
##        x.state = slot_value
##        print (env_object); 
        print ('[motor - entering',slot_value, ']')
        self.parent.parent.vision_finst.state = 'finished'

#### This resets the finst state indicating the action is finished
#### Currently using the vision finst for all actions (so no interleaving or parallal)

    def vision_finst_reset(self):
        self.parent.parent.vision_finst.state = 're_set' # reset the vision_finst
        print('[motor module] vision_finst reset')
