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
        b_plan_unit_order.set('counter:one first:AK second:HW third:RP fourth:finished') ######## new buffer


    def START_RP(b_context='status:starting_game planning_unit:none',
                 b_unit_task='unit_task:START state:running',
                 b_method='state:finished', b_visual='RP'):  ###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        b_plan_unit.modify(planning_unit='RP',cuelag='none',cue='start',unit_task='RP',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print ('run_RP_PU')
        b_plan_unit_order.set('counter:one first:RP second:HW third:AK fourth:finished') ######## new buffer


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

    def request_second_unit_task(b_plan_unit='state:running',
                                 b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:one first:?first second:?second third:?third fourth:?fourth'):
        b_unit_task.set('unit_task:?second state:start type:ordered')
        b_plan_unit_order.modify(counter='two')
        print ('fast - start second unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2222222222222222222222222222')

    def request_third_unit_task(b_plan_unit='state:running',
                                b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                b_plan_unit_order='counter:two first:?first second:?second third:?third fourth:?fourth',):
        b_unit_task.set('unit_task:?third state:start type:ordered')
        b_plan_unit_order.modify(counter='three')
        print ('fast - start third unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 333333333333333333333333333333')

    def request_fourth_unit_task(b_plan_unit='state:running',
                                 b_unit_task='unit_task:?unit_task state:finished type:ordered',
                                 b_plan_unit_order='counter:three first:?first second:?second third:?third fourth:?fourth'):
        b_plan_unit_order.modify(counter='four')
        b_unit_task.set('unit_task:?fourth state:start type:ordered')
        print ('fast - start third unit task >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 444444444444444444444444444444')

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

# AK unit task AK-WM-SU-ZB-FJ

## add condition to fire this production

    def AK_ordered(b_unit_task='unit_task:AK state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        b_unit_task.modify(state='begin')
        print ('start unit task AK')

    ## the first production in the unit task must begin this way
    def AK_start(b_unit_task='unit_task:AK state:begin type:?type'):
        b_unit_task.set('unit_task:AK state:running2 type:?type')
        b_method.set('method:response target:response content:1234 state:start')
##        focus.set('AKstart')
        print ('AK:1234')

    ## body of unit task
    #### RESPOND WM:
    def AK_WM(b_unit_task='unit_task:AK state:running2 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:1432 state:start')
        b_unit_task.set('unit_task:AK state:running3 type:?type')
        print ('WM:1432')

    #### RESPOND SU:
    def AK_SU(b_unit_task='unit_task:AK state:running3 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
        b_unit_task.set('unit_task:AK state:running4 type:?type')
        print ('SU:4123')

    #### RESPOND ZB:
    def AK_ZB(b_unit_task='unit_task:AK state:running4 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
        b_unit_task.set('unit_task:AK state:running5 type:?type')
        print ('ZB:2143')

    ### RESPOND FJ
    def AK_FJ(b_unit_task='unit_task:AK state:running5 type:?type',
                   b_method='state:finished',
                   focus='response_entered'):
        b_method.set('method:response target:response content:3214 state:start')
        ### FOCUS SET TO END
        focus.set('AK_done')
        b_unit_task.set('unit_task:AK state:end_task type:ordered')  ## this line ends the unit task
        print ('FJ:3214')
        print ('Ending Unit Task')

    ### RUN GET CODE METH
    ##### AK FINISH #####
    ### Final step:
    ## Finishing the unit task
    def AK_finished_ordered(
        b_method='state:finished',
                                ## this line assumes waiting for the last method to finish
                                focus='response_entered',
                                b_unit_task='unit_task:AK state:end_task type:ordered',
                                b_plan_unit='ptype:ordered'):
        print ('finished unit task AK(ordered)')
        b_unit_task.set('unit_task:AK state:finished type:ordered')

########################
##### RP Unit Task #####
########################

#                    YP-FJ
# RP unit task RP-SU<
#                    ZB-WM


# add condition to fire production
    def RP_ordered(b_unit_task='unit_task:RP state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        b_unit_task.modify(state='begin')
        print ('start unit task RP')

    ## the first production in the unit task must begin this way
    def RP_start(b_unit_task='unit_task:RP state:begin type:?type'):
        b_unit_task.set('unit_task:RP state:running type:?type')
        b_method.set('method:response target:response content:4321 state:start')
        focus.set('RPstart')
        print ('RP:4321')

    ##### RP BODY: #####
    ### PROMPT 1 - KNOWN, FAST
    def RP_SU(b_unit_task='unit_task:RP state:running type:?type',
                   b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
        b_unit_task.set('unit_task:RP state:running2 type:?type')
        print ('SU:4123')

        ## Prompt 1 = running perfect.

    ##### RP PROMPT 2 #####
    ### IDENTIFY -> RESPOND
    ### ROUND 2 - TWO POSSIBLE, KNOWN, LAG
    ### IDENTIFY:
    def RP_identify2(b_unit_task='unit_task:RP state:running2 type:?type',
                            focus='response_entered', b_method='state:finished'):
        b_method.set('method:get_code target:response content:0000 state:start')
        focus.set('get_code')
        b_unit_task.set('unit_task:RP state:runningC type:?type')
        print ('waiting to see if YP or ZB')
        print ('getting the code for second prompt...')

    #### RESPOND YP:
    def RP_YP(b_unit_task='unit_task:RP state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:3412 state:start')
        b_unit_task.set('unit_task:RP state:running3 type:?type')
        print ('YP:3412')
        # next is FJ


    ### RESPOND ZB:
    def RP_ZB(b_unit_task='unit_task:RP state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
        b_unit_task.set('unit_task:RP state:running4 type:?type')
        print ('ZB:2143')
        # next is WM
        ### RUN GET CODE METH

    ##### RP PROMPT 3 #####
    ### ROUND 3:
    ### BANG BANG

    ### RESPOND FJ
    def RP_FJ(b_unit_task='unit_task:RP state:running3 type:?type',
                   focus='response_entered'):
        b_method.set('method:response target:response content:3214 state:start')
        ### FOCUS SET TO END
        focus.set('RP_done')
        b_unit_task.set('unit_task:RP state:end_task type:ordered')  ## this line ends the unit task
        print ('FJ:3214')
        print ('Ending Unit Task')

    ### RESPOND WM
    def RP_WM(b_unit_task='unit_task:RP state:running4 type:?type',
                   focus='response_entered'):
        b_method.set('method:response target:response content:1432 state:start')
        ### FOCUS SET TO END
        focus.set('RP_done')
        b_unit_task.set('unit_task:RP state:end_task type:ordered')  ## this line ends the unit task
        print ('WM:1432')
        print ('Ending Unit Task')

                ### RUN GET CODE METH
    ##### RP FINISH #####
    ### Final step:
    ## Finishing the unit task
    def RP_finished_ordered(
        b_method='state:finished',
                                ## this line assumes waiting for the last method to finish
                                focus='response_entered',
                                b_unit_task='unit_task:RP state:end_task type:ordered',
                                b_plan_unit='ptype:ordered'):
        print ('finished unit task RP(ordered)')
        b_unit_task.set('unit_task:RP state:finished type:ordered')

########################
##### HW Unit Task #####
########################

#                     / FJ
# HW unit task HW-YP--- ZB
#                     \ SU

# add condition to fire production
    def HW_ordered(b_unit_task='unit_task:HW state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        b_unit_task.modify(state='begin')
        print ('start unit task HW')

    ## the first production in the unit task must begin this way
    def HW_start(b_unit_task='unit_task:HW state:begin type:?type'):
        b_unit_task.set('unit_task:HW state:running type:?type')
        b_method.set('method:response target:response content:2341 state:start')
        focus.set('HWstart')
        print ('HW:2341')


    ##### HW BODY: #####
    ### PROMPT 1 - KNOWN, FAST
    def HW_YP(b_unit_task='unit_task:HW state:running type:?type',
                   b_method='state:finished'):
        b_method.set('method:response target:response content:3412 state:start')
        b_unit_task.set('unit_task:HW state:running2 type:?type')
        print ('YP:3412')

        ## Prompt 1 = running perfect.

    ##### HW PROMPT 2 #####
    ### IDENTIFY -> RESPOND
    ### ROUND 2 - THREE POSSIBLE, KNOWN, LAG
    ### IDENTIFY:
    def HW_identify3(b_unit_task='unit_task:HW state:running2 type:?type',
                            focus='response_entered', b_method='state:finished'):
        b_method.set('method:get_code target:response content:0000 state:start')
        focus.set('get_code')
        b_unit_task.set('unit_task:HW state:runningC type:?type')
        print ('waiting to see if FJ, SU, or ZB')
        print ('getting the code for second prompt...')

    #### FJ RESPOND:
    def HW_FJ(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:3214 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print ('FJ:3214')
        print ('Ending Unit Task')


    #### SU RESPOND:
    def HW_SU(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print ('SU:4123')
        print ('Ending Unit Task')

    #### ZB RESPOND:
    def HW_ZB(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print ('ZB:2143')
        print ('Ending Unit Task')

                    ### RUN GET CODE METH
    ##### HW FINISH #####
    ### Final step:
    ## Finishing the unit task
    def HW_finished_ordered(
        b_method='state:finished',
                                ## this line assumes waiting for the last method to finish
                                focus='response_entered',
                                b_unit_task='unit_task:HW state:end_task type:ordered',
                                b_plan_unit='ptype:ordered'):
        print ('finished unit task HW(ordered)')
        b_unit_task.set('unit_task:HW state:finished type:ordered')

###################
##### METHODS #####
###################

    ### RESPONSE TYPE: IDENTIFY->RESPOND
    ### get_code method ################################ (get_code)
    # in the case where the next response depends on the code the agent must first read the code
    # AKA - this is the instance where the agent is not predicting the next response
    # but reading->chosing
    # The different pace times are accounting for the lag - LOW
    # This method is inseperable, and ordered
    ### PART A: IDENTIFY CODE

    def get_code_vision(b_method='method:get_code target:?target content:?content state:start'):  # target is the chunk to be altered
        motor.see_code()
        b_method.modify(state='running')
        print ('getting code')

    def get_code_finished(vision_finst='state:see_code'):
        motor.vision_finst_reset()
        b_method.modify(state='finished')
        focus.set('code:identified')
        print ('I have seen the code')




    ### PART B: response known , hit it
    # in this case the vision component took place already using the get_code method so this is only motor

    def response(b_method='method:response target:?target content:?content state:start'):  # target is the chunk to be altered
        motor.enter_response(target, content)
        RT.recordRT(content) # Record a reaction time after a response is entered
        b_method.modify(state='running')
        focus.set('enter_complete')
        print ('entering response')
        print ('target object = ', target)

    def response_entered2(b_method='method:?method target:?target state:running',
                          vision_finst='state:enter_response',
                          focus='enter_complete'):
        b_method.modify(state='finished')
        focus.set('response_entered')
        motor.vision_finst_reset()
        print ('I have altered', target)
