import sys
import ccm
from EmilyMotorModule import *
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
    motor = EmilyMotorModule(b_motor)

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

    def START_start(b_context='status:unoccupied planning_unit:none'):
        b_unit_task.set('unit_task:START state:running')
        b_context.modify(status='starting_game')
        print ('waiting to see code')
        motor.see_code()


    def START_AK(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished',
                 b_visual='AK'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='AK',cuelag='none',cue='start',unit_task='AK',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print ('run_AK_PU')
        b_plan_unit_order.set('counter:one first:AK second:HW third:RP fourth:finished') ######## new buffer


    def START_RP(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished',
                 b_visual='RP'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='RP',cuelag='none',cue='start',unit_task='RP',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print ('run_RP_PU')
        b_plan_unit_order.set('counter:one first:RP second:HW third:AK fourth:finished') ######## new buffer


    def START_HW(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished',
                 b_visual='HW'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        print ('fast - start first unit task')

    def request_second_unit_task(b_plan_unit='state:running',
                                 b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:one first:?first second:?second third:?third fourth:?fourth'):
        b_unit_task.set('unit_task:?second state:start type:ordered')
        b_plan_unit_order.modify(counter='two')
        print ('fast - start second unit task')

    def request_third_unit_task(b_plan_unit='state:running',
                                b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                b_plan_unit_order='counter:two first:?first second:?second third:?third fourth:?fourth',):
        b_unit_task.set('unit_task:?third state:start type:ordered')
        b_plan_unit_order.modify(counter='three')
        print ('fast - start third unit task')

    def request_fourth_unit_task(b_plan_unit='state:running',
                                 b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:three first:?first second:?second third:?third fourth:?fourth'):
        b_plan_unit_order.modify(counter='four')
        b_unit_task.set('unit_task:?fourth state:start type:ordered')
        print ('fast - start third unit task')

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
        print ('next code is')
        print (x)
        motor.referee_action('display', 'state', x)


#################
##### AK UT #####
#################

# AK unit task AK-WM-SU-ZB-FJ

## add condition to fire this production

    def AK_ordered(b_unit_task='unit_task:AK state:start type:ordered'):
        b_unit_task.modify(state='begin')
        print ('start unit task AK')

    def AK_start(b_unit_task='unit_task:AK state:begin'):
        b_unit_task.set('unit_task:AK state:running')
        focus.set('AK')
        target='responce'
        content='AK-AK-1234'
        motor.enter_response(target, content)

    def AK_WM(b_unit_task='unit_task:AK state:running',
              vision_finst='state:finished',
              focus='AK'):
        focus.set('WM')
        target='responce'
        content='AK-WM-1432'
        motor.enter_response(target, content)
        
    def AK_SU(b_unit_task='unit_task:AK state:running',
              vision_finst='state:finished',
              focus='WM'):
        focus.set('SU')
        target='responce'
        content='AK-SU-4123'
        motor.enter_response(target, content)

    def AK_ZB(b_unit_task='unit_task:AK state:running',
              vision_finst='state:finished',
              focus='SU'):
        focus.set('ZB')
        target='responce'
        content='AK-ZB-2143'
        motor.enter_response(target, content)

    def AK_FJ(b_unit_task='unit_task:AK state:running',
              vision_finst='state:finished',
              focus='ZB'):
        focus.set('done')
        target='responce'
        content='AK-FJ-3214'
        motor.enter_response(target, content)

    def AK_finished_ordered(b_unit_task='unit_task:AK state:running',
                            vision_finst='state:finished',
                            focus='done'):
        print ('finished unit task AK(ordered)')
        b_unit_task.set('unit_task:AK state:finished type:ordered')



########################
##### RP Unit Task #####
########################

#                    YP-FJ
# RP unit task RP-SU<
#                    ZB-WM

    def RP_ordered(b_unit_task='unit_task:RP state:start type:ordered'):
        b_unit_task.modify(state='begin')
        print ('start unit task RP')

    def RP_start(b_unit_task='unit_task:RP state:begin'):
        b_unit_task.set('unit_task:RP state:running')
        focus.set('RP')
        target='responce'
        content='RP-RP-4321'
        motor.enter_response(target, content)

    def RP_SU(b_unit_task='unit_task:RP state:running',
              vision_finst='state:finished',
              focus='RP'):
        focus.set('SU')
        target='responce'
        content='RP-SU-4123'
        motor.enter_response(target, content)

    ### Unkown code
        
    def RP_identify2(b_unit_task='unit_task:RP state:running',
                     vision_finst='state:finished',
                     focus='SU'):
        ############################### referee
        choices = ['YP','ZB']
        x=random.choice(choices)
        motor.referee_action('display', 'state', x)
        ############################### referee        
        motor.see_code()
        focus.set('code_seen')
        print ('waiting to see if YP or ZB')

    def RP_YP(b_unit_task='unit_task:RP state:running',
              vision_finst='state:finished',
              focus='code_seen',
              b_visual='YP'):
        focus.set('done')
        target='responce'
        content='RP-YP-3412'
        motor.enter_response(target, content)

    def RP_ZB(b_unit_task='unit_task:RP state:running',
              vision_finst='state:finished',
              focus='code_seen',
              b_visual='ZB'):
        focus.set('done')
        target='responce'
        content='RP-ZB-2143'
        motor.enter_response(target, content)

    def RP_FJ(b_unit_task='unit_task:RP state:running',
              vision_finst='state:finished',
              focus='YP'):
        focus.set('done')
        target='responce'
        content='RP-FJ-3214'
        motor.enter_response(target, content)

    def RP_WM(b_unit_task='unit_task:RP state:running',
              vision_finst='state:finished',
              focus='ZB'):
        focus.set('done')
        target='responce'
        content='RP-WM-1432'
        motor.enter_response(target, content)

    def RP_finished_ordered(b_unit_task='unit_task:RP state:running',
                            vision_finst='state:finished',
                            focus='done'):
        print ('finished unit task RP(ordered)')
        b_unit_task.set('unit_task:RP state:finished type:ordered')

########################
##### HW Unit Task #####
########################

#                     / FJ
# HW unit task HW-YP--- ZB
#                     \ SU

    def HW_ordered(b_unit_task='unit_task:HW state:start type:ordered'):
        b_unit_task.modify(state='begin')
        print ('start unit task HW')

    ## the first production in the unit task must begin this way
    def HW_start(b_unit_task='unit_task:HW state:begin'):
        b_unit_task.set('unit_task:HW state:running')
        focus.set('HW')
        target='responce'
        content='HW-HW-2341'
        motor.enter_response(target, content)

    def HW_YP(b_unit_task='unit_task:HW state:running',
              vision_finst='state:finished',
              focus='HW'):
        focus.set('YP')
        target='responce'
        content='HW-YP-3412'
        motor.enter_response(target, content)

    ### Unkown code
        
    def HW_identify3(b_unit_task='unit_task:HW state:running',
                     vision_finst='state:finished',
                     focus='YP'):
        ############################### referee
        choices = ['FJ','SU','ZB']
        x=random.choice(choices)
        motor.referee_action('display', 'state', x)
        ############################### referee        
        motor.see_code()
        focus.set('code_seen')
        print ('waiting to see if FJ, SU, or ZB')
        

    #### FJ or SU or ZB then end
        
    def HW_FJ(b_unit_task='unit_task:HW state:running',
              vision_finst='state:finished',
              focus='code_seen',
              b_visual='FJ'):
        focus.set('done')
        target='responce'
        content='HW-FJ-3214'
        motor.enter_response(target, content)


    def HW_SU(b_unit_task='unit_task:HW state:running',
              vision_finst='state:finished',
              focus='code_seen',
              b_visual='SU'):
        focus.set('done')
        target='responce'
        content='HW-SU-4123'
        motor.enter_response(target, content)


    def HW_ZB(b_unit_task='unit_task:HW state:running',
              vision_finst='state:finished',
              focus='code_seen',
              b_visual='ZB'):
        focus.set('done')
        target='responce'
        content='HW-ZB-2143'
        motor.enter_response(target, content)

    def HW_finished_ordered(b_unit_task='unit_task:HW state:running',
                            vision_finst='state:finished',
                            focus='done'):
        print ('finished unit task HW(ordered)')
        b_unit_task.set('unit_task:HW state:finished type:ordered')

