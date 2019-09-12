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

def move_object():
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))

	#Moving object from position 1 to position 2
    dxl_io.set_goal_position(dict(zip([8, 9], [60, 30])))
    time.sleep(1)
    
move_object()