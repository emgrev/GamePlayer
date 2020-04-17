import sys
import ccm
from MotorModule import *
from RTModule import *
from ccm.lib.actr import *
from random import randrange, uniform

#####################
##### The Agent #####
#####################

class MyAgent(ACTR):

# BUFFERS
    focus=Buffer()
    b_context = Buffer()
    b_plan_unit = Buffer()
    b_plan_unit_order = Buffer()
    b_unit_task = Buffer()
    b_method = Buffer()
    b_operator = Buffer()
    b_DM = Buffer()
    b_motor = Buffer()
    b_visual = Buffer()

    # visual = Buffer()

# MODULES (import modules into agent, connect to buffers, and add initial content)

    # motor module - defined above
    motor = MotorModule(b_motor)

    # declarative memory module - from CCM suite
    DM = Memory(b_DM)

    # reation time module - used to record the reaction time of the agent
    RT = RTModule()

    # initial buffer contents
    b_context.set('status:unoccupied planning_unit:none')
    b_plan_unit.set('planning_unit:P cuelag:P cue:P unit_task:P state:P ptype:P')
    b_visual.set('00')
    focus.set('start')
    b_plan_unit_order.set('counter:oo first:oo second:oo third:oo fourth:oo')


    def START(focus='start'):
        print ('1')
        focus.set('a:aaa b:bbb c:ccc')


    def TWO(focus='a:aaa b:?b'): 
        print ('2')
        print(b)
        #focus.modify(a=b)
        focus.set('a:?b')


    def THREE(focus='a:bbb'):
        print('3')

########## unit task management productions ###########

######################### these manage the sequence if it is an ordered planning unit stored in buffer

    def setup_first_unit_task(b_plan_unit='unit_task:?unit_task state:begin_sequence ptype:ordered'):
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        b_plan_unit.modify(state='running')
        print ('fast - start first unit task 11111111111111111111111111111111111111111111111111111111111111111111111111111')

    def request_second_unit_task(b_plan_unit='unit_task:?unit_task state:running',
                                 b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:one first:?first second:?second third:?third fourth:?fourth'):
        b_unit_task.set('unit_task:HW state:start type:ordered') ## problem passing ?second
        b_plan_unit_order.modify(counter='two')
        print ('fast - start second unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2222222222222222222222222222')
        print (second)

    def request_third_unit_task(b_plan_unit='unit_task:?unit_task state:running',
                                b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                b_plan_unit_order='counter:two first:?first second:?second third:?third fourth:?fourth'):
        b_plan_unit_order.modify(counter='end')
##        b_plan_unit.modify(state='running')
##        b_unit_task.set('unit_task:?second state:start type:ordered')
##        b_plan_unit_order.set('counter:two first:?first second:?second third:?third fourth:?fourth')
        print ('fast - start third unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 333333333333333333333333333333')
        print ('third')











