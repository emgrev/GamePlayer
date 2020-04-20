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

    # initial memory contents

    DM.add('planning_unit:AK         cuelag:none          cue:start          unit_task:AK')
    DM.add('planning_unit:AK         cuelag:start         cue:AK              unit_task:HW')
    DM.add('planning_unit:AK         cuelag:AK             cue:HW              unit_task:RP')
    DM.add('planning_unit:AK         cuelag:HW              cue:RP              unit_task:finished')

    DM.add('planning_unit:RP         cuelag:none          cue:start          unit_task:RP')
    DM.add('planning_unit:RP         cuelag:start         cue:RP              unit_task:HW')
    DM.add('planning_unit:RP         cuelag:RP             cue:HW              unit_task:AK')
    DM.add('planning_unit:RP         cuelag:HW              cue:AK              unit_task:finished')

    DM.add('planning_unit:HW         cuelag:none          cue:start          unit_task:HW')
    DM.add('planning_unit:HW         cuelag:start         cue:HW              unit_task:RP')
    DM.add('planning_unit:HW         cuelag:HW             cue:RP              unit_task:AK')
    DM.add('planning_unit:HW         cuelag:RP              cue:AK              unit_task:finished')

##    DM.add('planning_unit:start_game      cuelag:none          cue:start          unit_task:START')
##    DM.add('planning_unit:start_game      cuelag:start         cue:no_cue            unit_task:finished')

## this could be used, but instead the code goes straight to the START uniti task

########### create productions for choosing planning units ###########

    ## these productions are the highest level of SGOMS and fire off the context buffer
    ## they can take any ACT-R form (one production or more) but must eventually call a planning unit and update the context buffer




    def START_AK(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished', b_visual='AK'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='AK',cuelag='none',cue='start',unit_task='AK',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print ('run_AK_PU')
        b_plan_unit_order.set('counter:one first:AK second:HW third:RP fourth:end') ######## new buffer


    def START_RP(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished', b_visual='RP'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='RP',cuelag='none',cue='start',unit_task='RP',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print ('run_RP_PU')
        b_plan_unit_order.set('counter:one first:RP second:HW third:AK fourth:end') ######## new buffer


    def START_HW(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished', b_visual='HW'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='HW',cuelag='none',cue='start',unit_task='HW',state='begin_sequence',ptype='ordered')
        b_plan_unit_order.set('counter:one first:HW second:RP third:AK fourth:finished') ######## new buffer
        b_context.modify(status='occupied')
        print ('run_HW_PU')
        print

########## unit task management productions ###########

######################### these manage the sequence if it is an ordered planning unit stored in DM

## removed

######################### these manage the sequence if it is an ordered planning unit stored in buffer

    def setup_first_unit_task(b_plan_unit='unit_task:?unit_task state:begin_sequence ptype:ordered'):
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        b_plan_unit.modify(state='running')
        print ('fast - start first unit task 11111111111111111111111111111111111111111111111111111111111111111111111111111')

    def request_second_unit_task(#b_plan_unit='state:running',
                                 #b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:one first:?first second:?second third:?third fourth:?fourth'):
        b_unit_task.set('unit_task:?second state:start type:ordered')
        b_plan_unit_order.modify(counter='two')
        print ('fast - start second unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2222222222222222222222222222')

    def request_third_unit_task(#b_plan_unit='state:running',
                                #b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                b_plan_unit_order='counter:two first:?first second:?second third:?third fourth:?fourth',):
        b_unit_task.set('unit_task:?third state:start type:ordered')
        b_plan_unit_order.modify(counter='one')
        print ('fast - start third unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 333333333333333333333333333333')

    def request_fourth_unit_task(b_plan_unit_order='counter:three first:?first second:?second third:?third fourth:?fourth'):
##        b_plan_unit_order.modify(counter='four')
##        b_unit_task.set('unit_task:?fourth state:start type:ordered')
        print ('fast - start fourth unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 444444444444444444444444444444')

########################## these manage planning units that are finished ###################

    def last_unit_task_ordered_plan(b_plan_unit='planning_unit:?planning_unit',
                                    b_unit_task='unit_task:finished state:start type:ordered'):
        print ('finished planning unit =')
        print (planning_unit)
        b_unit_task.set('stop')
        b_context.modify(status='unoccupied')
        ############################### referee
        choices = ['AK','RP','HW']
        x=random.choice(choices)
        print ('next code is &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print (x)
        motor.referee_action('display', 'state', x)
        ################################


#################
##### START UT ##
#################

## this unit task fires from the starting condition and puts the code in the visual buffer
## in its current form it is a hack and not a proper unit task

    def START_start(b_context='status:unoccupied planning_unit:none'):
        b_method.set('method:get_code target:response content:0000 state:start')
        b_unit_task.set('unit_task:START state:running')
        b_context.modify(status='starting_game')
        print ('waiting to see code')

#################
##### AK UT #####
#################

    def AK_ordered(b_unit_task='unit_task:AK state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        print ('finished unit task AK(ordered)')
        b_unit_task.set('unit_task:AK state:finished type:ordered')

########################
##### RP Unit Task #####
########################

# add condition to fire production
    def RP_ordered(b_unit_task='unit_task:RP state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        print ('finished unit task RP(ordered)')
        b_unit_task.set('unit_task:RP state:finished type:ordered')

########################
##### HW Unit Task #####
########################

# add condition to fire production
    def HW_ordered(b_unit_task='unit_task:HW state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        print ('finished unit task HW(ordered)')
        b_unit_task.set('unit_task:HW state:finished type:ordered')


