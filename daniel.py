#this is a test of motors for Philos' arms and neck
#this test goal is to test if motors can work and can let Philos do some gestures
#this test is tested by Leo(Xiao)
import itertools
import numpy as np
import time
import serial

import pypot.dynamixel
import time



ports = pypot.dynamixel.get_available_ports()
print('available ports:', ports)  

if not ports:
    raise IOError('No port available.') 

port = ports[1]
print('Using the first on the list', port)

dxl_io = pypot.dynamixel.DxlIO(port)
print('Connected!')

found_ids = dxl_io.scan(range(13))
print('Found ids:', found_ids)

if len(found_ids) < 2:
    raise IOError('You should connect at least two motors on the bus for this test.')
#chose all motors and enable torque and set the same speed
ids = found_ids[:]
dxl_io.enable_torque(ids)
speed = dict(zip(ids, itertools.repeat(20)))
dxl_io.set_moving_speed(speed)
dxl_io.set_moving_speed(dict(zip([1,2], itertools.repeat(15))))
dxl_io.set_moving_speed(dict(zip([3,8], itertools.repeat(25))))


# GPIO.setmode(GPIO.BOARD)
# servo1=7
# servo2=11
# GPIO.setup(servo1,GPIO.OUT)
# GPIO.setup(servo2,GPIO.OUT)
# pwm1=GPIO.PWM(servo1,50)
# pwm2=GPIO.PWM(servo2,50)
# pwm1.start(7)
# pwm2.start(7)
# time.sleep(1)
# desiredPosition1 = 10
# desiredPosition2 = 35
# DC1=1./18.*(desiredPosition1+90)+1
# DC2=1./18.*(desiredPosition2+90)+1
# pwm1.ChangeDutyCycle(DC1)
# pwm2.ChangeDutyCycle(DC2)
# time.sleep(1)
    

#set stater pose for each motor
start_pose=[ -55.28, -9.53, 45.6, 30.06, -7.48, 49.12, -46.77, -44.13, -27.13, 8.94, -37.39, 50.0]

def speed_traj(ID, stepsize, begin_pose, end_pose, v_max):
    speed = 0
    pose = begin_pose
    t = round(2*abs(end_pose-begin_pose)/v_max,2)
    t1 = round(t/2,2)
    t2 = t
    print('t2',t)
    a = np.arange(0,t1,stepsize)
    for t in range (a.shape[0]):
        speed = v_max/(t1/stepsize)+speed
        print('speed1',speed)
        pose = pose+ (abs(end_pose-begin_pose)/(end_pose-begin_pose))*speed*stepsize
        time.sleep(stepsize)
        dxl_io.set_moving_speed(dict(zip([ID], itertools.repeat(speed))))
        dxl_io.set_goal_position(dict(zip([ID], [pose])))
        print('pose',pose)
    for t in range (a.shape[0]):
        speed = speed - v_max/((t2-t1)/stepsize)
        print('speed2',speed)
        pose = pose+ (abs(end_pose-begin_pose)/(end_pose-begin_pose))*speed*stepsize
        time.sleep(stepsize)
        dxl_io.set_moving_speed(dict(zip([ID], itertools.repeat(speed))))
        dxl_io.set_goal_position(dict(zip([ID], [pose])))
        

def test():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
    speed_traj(1, 0.25, -55.28, -15, 45)
    time.sleep(0.5)
    speed_traj(1, 0.25, -15, -90, 45)
    print("finish test")





#define functions of different behavior
def hello():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
##        dxl_io.set_goal_position(dict(zip([1], [-10])))
##        time.sleep(2)
##        dxl_io.set_goal_position(dict(zip([1], [-80])))
##        time.sleep(2)
    
    # nodding
    dxl_io.set_goal_position(dict(zip([2], [16.25])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([2], [-9.53])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([2], [16.25])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([2], [-9.53])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([2], [16.25])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([2], [-9.53])))
    time.sleep(1)


    # waiving hand
    dxl_io.set_moving_speed(dict(zip([3], itertools.repeat(55))))
    dxl_io.set_goal_position(dict(zip([3], [-70])))
    time.sleep(3)
    dxl_io.set_moving_speed(dict(zip([5], itertools.repeat(65))))
    dxl_io.set_goal_position(dict(zip([5], [-36.22])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-7.48])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-36.22])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-7.48])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-36.22])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-7.48])))
    time.sleep(0.5)
    dxl_io.set_moving_speed(dict(zip([3], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([3], [32.7])))
    time.sleep(1.5)
    dxl_io.set_goal_position(dict(zip([3], [40])))
    time.sleep(1.5)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)

    print('Philo says hi')


def hugging():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)
    dxl_io.set_goal_position(dict(zip([2], [16.25])))
    time.sleep(2)
    dxl_io.set_goal_position(dict(zip([2], [-9.53])))
    time.sleep(1)


    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(60))))
    dxl_io.set_goal_position(dict(zip([3, 8], [-10, 10])))
    time.sleep(3)
    dxl_io.set_moving_speed(dict(zip([4,9], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([4, 9], [58.21, -62.02])))
    time.sleep(3)
    dxl_io.set_moving_speed(dict(zip([7,12], itertools.repeat(60))))
    dxl_io.set_goal_position(dict(zip([7, 12], [-21.85, -24.78])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([7, 12], [-46.77, 50.0])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([7, 12], [-21.85, -24.78])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([7, 12], [-46.77, 50.0])))
    time.sleep(0.5)

    
    dxl_io.set_goal_position(dict(zip([4, 9], [30.06, -27.13])))
    time.sleep(2)
    dxl_io.set_goal_position(dict(zip([4, 9], [58.21, -62.02])))
    time.sleep(3)
    dxl_io.set_goal_position(dict(zip([4, 9], [30.06, -27.13])))
    time.sleep(2)
    dxl_io.set_moving_speed(dict(zip([3,8], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([3,8], [32.7, -32.11])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)
    print('Philo is hugging hands with you')

#NEW CODE BEGINS HERE
def hand_shaking():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
    dxl_io.set_moving_speed(dict(zip([8], itertools.repeat(60))))
    dxl_io.set_goal_position(dict(zip([8], [15.69])))
    time.sleep(2.5)
    dxl_io.set_moving_speed(dict(zip([10], itertools.repeat(55))))
    dxl_io.set_goal_position(dict(zip([10], [62.32])))
    time.sleep(1.5)
    dxl_io.set_moving_speed(dict(zip([12], itertools.repeat(60))))
    dxl_io.set_goal_position(dict(zip([12], [0])))
    time.sleep(0.5)
    dxl_io.set_moving_speed(dict(zip([8], itertools.repeat(40))))
    dxl_io.set_goal_position(dict(zip([8], [-5])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([8], [15.69])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([8], [-5])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([8], [15.69])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip([12], [50])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([10], [8.94])))
    time.sleep(1.5)
    dxl_io.set_goal_position(dict(zip([8], [-35])))
    time.sleep(1.5)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)

def thank_you():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(55))))
    dxl_io.set_goal_position(dict(zip([3, 8], [23.8, -24.19])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([2, 3, 8], [-9.53, -2.79, 2.49])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([2], [16.25])))
    time.sleep(0.5)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([3, 8], [32.7, -32.11])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)

def dance2():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(55))))
    dxl_io.set_goal_position(dict(zip([3, 8], [1.32, -6.83])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5, 10], [-64.06, 63.78])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([3, 8], [-86.07, 87.54])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([1, 5, 10], [-81.96, -38.27, 39.85])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([1, 5, 10], [-6.3, -89.88, 43.84])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([1, 5, 10], [-81.96, -38.27, 39.85])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([1, 5, 10], [-6.3, -89.88, 43.84])))
    time.sleep(0.5)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([3, 8], [32.7, -32.11])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)

def dance3():
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(1.5)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(55))))
    dxl_io.set_goal_position(dict(zip([3, 8], [4.84, -5.43])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5, 10, 7, 12], [-39.15, 45.01, -12.40, 8.05])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [16.25])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-39.15])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([10], [-59.09])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([10], [45.01])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [16.25])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([5], [-39.15])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([10], [-59.09])))
    time.sleep(0.5)
    dxl_io.set_goal_position(dict(zip([10], [45.01])))
    time.sleep(1)
    dxl_io.set_moving_speed(dict(zip([3, 8], itertools.repeat(30))))
    dxl_io.set_goal_position(dict(zip([3, 8], [32.7, -32.11])))
    time.sleep(1)
    dxl_io.set_goal_position(dict(zip(ids, start_pose)))
    time.sleep(2)

hello()
#hugging()
#hand_shaking()
#thank_you()
dance2()
dance3()