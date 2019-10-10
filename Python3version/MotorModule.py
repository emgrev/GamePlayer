import sys
import ccm
from ccm.lib.actr import *
from random import randrange, uniform

########################
##### MOTOR MODULE #####
########################

class MotorModule(ccm.Model): # defines actions in the environment

    def change_b_vision(self):
        print ("Planning Unit Selection !!!!!!!!!!!!")
        self.parent.visual.set('AK')


# change_state is a generic action that changes the state slot of any object
# disadvantages (1) yield #time is always the same (2) cannot use for parallel actions


    def enter_response(self, env_object, slot_value):
        yield 3
        x = eval('self.parent.parent.' + env_object)
        x.state = slot_value
        print (env_object)
        print (slot_value)
        self.parent.parent.motor_finst.state = 'enter_response'

## Visual Cues
##### Type 1: ACTIVE TASK
    def see_code(self):
        yield 5
        print ('Object Identified')
        self.parent.parent.motor_finst.state = 'see_code'
        self.parent.visual = 'spotted'


#### movement

    def motor_finst_reset(self):
        self.parent.parent.motor_finst.state = 're_set'
