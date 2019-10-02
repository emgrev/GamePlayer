import sys
import ccm
from MotorModule import *
from ccm.lib.actr import *
from random import randrange, uniform

#####################
##### The Agent #####
#####################

class MyAgent(ACTR):

# BUFFERS (create buffers and add initial content)
    focus=Buffer()
    motor=MotorModule()

##    VMbuffer=Buffer()
##    VM-Memory(VMbuffer)

    DMbuffer=Buffer()
    DM=Memory(DMbuffer)

    # goal system buffers
    b_context = Buffer()
    b_plan_unit = Buffer()
    b_unit_task = Buffer()
    b_method = Buffer()
    b_operator = Buffer()

    # module Buffers
    b_DM = Buffer()
    b_motor = Buffer()
    visual = Buffer()

    # initial buffer contents
    b_context.set('status:start have_plan:no planning_unit:none')
    b_plan_unit.set('planning_unit:P cuelag:P cue:P unit_task:P state:P ptype:P')


# MODULES (import modules into agent, connect to buffers, and add initial content)

    # vision module - from CCM suite
    vision_module=SOSVision(visual,delay=.085)

    # motor module - defined above
    motor = MotorModule(b_motor)

    # declarative memory module - from CCM suite
    DM = Memory(b_DM)


    # initial memory contents
##        DM.add('planning_unit:XY         cuelag:none          cue:start          unit_task:X')
##        DM.add('planning_unit:XY         cuelag:start         cue:X              unit_task:Y')
##        DM.add('planning_unit:XY         cuelag:X             cue:Y              unit_task:finished')

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

    DM.add('planning_unit:start      cuelag:none          cue:start          unit_task:part_1')
    DM.add('planning_unit:start      cuelag:start         cue:wait            unit_task:finished')


########### create productions for choosing planning units ###########

    ## these productions are the highest level of SGOMS and fire off the context buffer
    ## they can take any ACT-R form (one production or more) but must eventually call a planning unit and update the context buffer

    def run_START_PU(b_context='status:start planning_unit:none'):
        b_plan_unit.modify(planning_unit='start',cuelag='none',cue='start',unit_task='part_1',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print 'STARTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'

    def run_AK_PU(b_context='status:unoccupied planning_unit:none'):
        b_plan_unit.modify(planning_unit='AK',cuelag='none',cue='start',unit_task='AK',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    def run_RP_PU(b_context='status:unoccupied planning_unit:none'):
        #b_context='status:unoccupied planning_unit:RP'):
        b_plan_unit.modify(planning_unit='RP',cuelag='none',cue='start',unit_task='RP',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'

    def run_HW_PU(b_context='status:unoccupied planning_unit:none'):
        #b_context='status:unoccupied planning_unit:HW'):
        b_plan_unit.modify(planning_unit='HW',cuelag='none',cue='start',unit_task='HW',state='begin_sequence',ptype='ordered')
        b_context.modify(status='occupied')
        print 'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'

#######################################################
########## unit task management productions ###########
#######################################################

    def setup_ordered_planning_unit(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:begin_sequence ptype:ordered'):
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        b_plan_unit.modify(state='running')
        print 'begin orderdered planning unit = ', planning_unit

######################### these manage the sequence if it is an ordered planning unit

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',
                               b_unit_task='unit_task:?unit_task state:finished type:ordered'):
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        b_plan_unit.modify(state='retrieve')
        print ' finished unit task = ', unit_task

    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):
        #b_plan_unit.modify(state='running')
        b_plan_unit.modify(planning_unit=planning_unit,cuelag=cuelag,cue=cue,unit_task=unit_task,state='running')
        b_unit_task.set('unit_task:?unit_task state:start type:ordered')
        print ' unit_task = ', unit_task

########################## these manage planning units that are finished ###################

    def last_unit_task_ordered_plan(b_context='have_plan:yes',
                                    b_plan_unit='planning_unit:?planning_unit',
                                    b_unit_task='unit_task:finished state:start type:ordered',
                                    utility=5):  # high priority if a plan was generated in the planning unit
        print 'finished planning unit=',planning_unit
        b_unit_task.set('stop')
        b_context.modify(status='unoccupied', have_plan='no') # have plan always needs to be re-set to no

    def last_unit_task_ordered_noplan(b_plan_unit='planning_unit:?planning_unit',
                                      b_unit_task='unit_task:finished state:start type:ordered',
                                      utility=1):  # by default no plan is generated
        print 'finished planning unit=',planning_unit
        b_unit_task.set('stop')
        #b_plan_unit.modify(planning_unit='none')
#        b_context.modify(planning_unit='none', have_plan='no') # have plan always needs to be re-set to no

#################### Stop Program ######################

    def stop_production(b_unit_task='stop'):
        print 'Task complete. Good bye!'
        self.stop()

#################################
##### Unit Task Productions #####
#################################

##### This UT should run every time the code is run
    # The sequence of this unit task is:
        # part 1 goes to the motor module --> use the motor module to put a PU in visual buffer
        # part 2 checks the visual buffer and activates the PU found

    # for preliminary tests I will just put the AK PU in the visual buffer
    def part_1(b_unit_task='unit_task:part_1 type:ordered'):
         print('putting AK in the visual buffer')
         motor.change_b_vision()
         b_unit_task.set('unit_task:part_2 type:ordered')

    def part_2(b_unit_task='unit_task:part_2 type:ordered'):
        vision_v = str(visual.chunk)
        print(vision_v)
        print('hopefully this runs')
        # need to check visual buffer
        # need to run PU based on that
        #STOPPPPPPPPPPPPPP
        b_plan_unit.set('planning_unit:' + vision_v +' cuelag:none cue:start unit_task:' + vision_v + ' state:begin_sequence ptype:ordered')
        # 'planning_unit:'+ vision_v +' cuelag:P cue:P unit_task:P state:P ptype:P'
        # in this line of code ^ if I can get planning unit:P to put what ever is in the visual buffer instead of P were in a good place
        b_unit_task.set('unit_task:stop')

#################
##### AK UT #####
#################

# AK unit task AK-WM-SU-ZB-FJ

## add condition to fire this production

    def AK_ordered(b_unit_task='unit_task:AK state:start type:ordered'): ### this unit task is chosen to fire by planning unit
        b_unit_task.modify(state='begin')
        print 'start unit task AK'

    ## the first production in the unit task must begin this way
    def AK_start(b_unit_task='unit_task:AK state:begin type:?type'):
        b_unit_task.set('unit_task:AK state:running2 type:?type')
        b_method.set('method:response target:response content:1234 state:start')
##        focus.set('AKstart')
        print 'AK:1234'

    ## body of unit task
    #### RESPOND WM:
    def AK_WM(b_unit_task='unit_task:AK state:running2 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:1432 state:start')
        b_unit_task.set('unit_task:AK state:running3 type:?type')
        print 'WM:1432'

    #### RESPOND SU:
    def AK_SU(b_unit_task='unit_task:AK state:running3 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
        b_unit_task.set('unit_task:AK state:running4 type:?type')
        print 'SU:4123'

    #### RESPOND ZB:
    def AK_ZB(b_unit_task='unit_task:AK state:running4 type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
        b_unit_task.set('unit_task:AK state:running5 type:?type')
        print 'ZB:2143'

    ### RESPOND FJ
    def AK_FJ(b_unit_task='unit_task:AK state:running5 type:?type',
                   b_method='state:finished',
                   focus='response_entered'):
        b_method.set('method:response target:response content:3214 state:start')
        ### FOCUS SET TO END
        focus.set('AK_done')
        b_unit_task.set('unit_task:AK state:end_task type:ordered')  ## this line ends the unit task
        print 'FJ:3214'
        print 'Ending Unit Task'

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
        print 'finished unit task RP(ordered)'
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
        print 'start unit task RP'

    ## the first production in the unit task must begin this way
    def RP_start(b_unit_task='unit_task:RP state:begin type:?type'):
        b_unit_task.set('unit_task:RP state:running type:?type')
        b_method.set('method:response target:response content:4321 state:start')
        focus.set('RPstart')
        print 'RP:4321'

    ##### RP BODY: #####
    ### PROMPT 1 - KNOWN, FAST
    def RP_SU(b_unit_task='unit_task:RP state:running type:?type',
                   b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
        b_unit_task.set('unit_task:RP state:running2 type:?type')
        print 'SU:4123'

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
        print 'waiting to see if YP or ZB'
        print 'getting the code for second prompt...'

    #### RESPOND YP:
    def RP_YP(b_unit_task='unit_task:RP state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:3412 state:start')
        b_unit_task.set('unit_task:RP state:running3 type:?type')
        print 'YP:3412'
        # next is FJ


    ### RESPOND ZB:
    def RP_ZB(b_unit_task='unit_task:RP state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
        b_unit_task.set('unit_task:RP state:running4 type:?type')
        print 'ZB:2143'
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
        print 'FJ:3214'
        print 'Ending Unit Task'

    ### RESPOND WM
    def RP_WM(b_unit_task='unit_task:RP state:running4 type:?type',
                   focus='response_entered'):
        b_method.set('method:response target:response content:1432 state:start')
        ### FOCUS SET TO END
        focus.set('RP_done')
        b_unit_task.set('unit_task:RP state:end_task type:ordered')  ## this line ends the unit task
        print 'WM:1432'
        print 'Ending Unit Task'

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
        print 'finished unit task RP(ordered)'
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
        print 'start unit task HW'

    ## the first production in the unit task must begin this way
    def HW_start(b_unit_task='unit_task:HW state:begin type:?type'):
        b_unit_task.set('unit_task:HW state:running type:?type')
        b_method.set('method:response target:response content:2341 state:start')
        focus.set('HWstart')
        print 'HW:2341'


    ##### HW BODY: #####
    ### PROMPT 1 - KNOWN, FAST
    def HW_YP(b_unit_task='unit_task:HW state:running type:?type',
                   b_method='state:finished'):
        b_method.set('method:response target:response content:3412 state:start')
        b_unit_task.set('unit_task:HW state:running2 type:?type')
        print 'YP:3412'

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
        print 'waiting to see if FJ, SU, or ZB'
        print 'getting the code for second prompt...'

    #### FJ RESPOND:
    def HW_FJ(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:3214 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print 'FJ:3214'
        print 'Ending Unit Task'


    #### SU RESPOND:
    def HW_SU(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:4123 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print 'SU:4123'
        print 'Ending Unit Task'

    #### ZB RESPOND:
    def HW_ZB(b_unit_task='unit_task:HW state:runningC type:?type',
                            b_method='state:finished'):
        b_method.set('method:response target:response content:2143 state:start')
                ### FOCUS SET TO END
        focus.set('HW_done')
        b_unit_task.set('unit_task:HW state:end_task type:ordered')  ## this line ends the unit task
        print 'ZB:2143'
        print 'Ending Unit Task'

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
        print 'finished unit task HW(ordered)'
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
        print 'getting code'

    def vision_slow_finished(motor_finst='state:see_code'):
        motor.motor_finst_reset()
        b_method.modify(state='finished')
        focus.set('code:identified')
        print 'I have spotted the target, I have the new code'

    ### PART B: response known , hit it
    # in this case the vision component took place already using the get_code method so this is only motor

    def response(b_method='method:response target:?target content:?content state:start'):  # target is the chunk to be altered
        motor.enter_response(target, content)
        b_method.modify(state='running')
        focus.set('enter_complete')
        print 'entering response'
        print 'target object = ', target

    def response_entered2(b_method='method:?method target:?target state:running',
                          motor_finst='state:enter_response',
                          focus='enter_complete'):
        b_method.modify(state='finished')
        focus.set('response_entered')
        motor.motor_finst_reset()
        print 'I have altered', target
