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

if len(found_ids) < 12:
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


def move_object_one_to_two():
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)

	#Moving arm to position 1
	dxl_io.set_goal_position(dict(zip([8], [10])))
	time.sleep(2)
	dxl_io.set_goal_position(dict(zip([9, 10], [-40, 50])))
	time.sleep(2)
	#Open hand
	dxl_io.set_goal_position(dict(zip([11, 12], [5, -50])))
	time.sleep(4)
	#Moving into position
	dxl_io.set_goal_position(dict(zip([8], [-15])))
	time.sleep(4)
	#Grabbing
	dxl_io.set_goal_position(dict(zip([12], [50])))
	time.sleep(4)
	#Moving back to position 2
	dxl_io.set_goal_position(dict(zip([8, 9, 10], [10, 12, 60])))
	time.sleep(4)
	#Lowering arm
	dxl_io.set_goal_position(dict(zip([8, 11], [-20, -20])))
	time.sleep(4)

	#Now, drop it!
	dxl_io.set_goal_position(dict(zip([12], [-50])))
	time.sleep(4)
			
	#to not hit the object
	dxl_io.set_goal_position(dict(zip([10], [50])))
	time.sleep(2)
	dxl_io.set_goal_position(dict(zip([8, 10], [10, 30])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([12], [40])))
	time.sleep(4)

	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)
	print("Object moved to center")

def move_object_two_to_one(): #This one is good, ready for compound testing
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)

	#Moving arm to position 2
	dxl_io.set_goal_position(dict(zip([8], [10])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([9, 10], [10, 45])))
	time.sleep(3)
	#Open hand 
	dxl_io.set_goal_position(dict(zip([11, 12], [-20, -50])))
	time.sleep(4)
	#Moving arm down
	dxl_io.set_goal_position(dict(zip([8], [-25])))
	time.sleep(3)
	#Grabbing
	dxl_io.set_goal_position(dict(zip([12], [70])))
	time.sleep(4)
	#Moving arm to position 1
	dxl_io.set_goal_position(dict(zip([8, 9, 10], [10, -50, 40])))
	time.sleep(4)
	#Lowering arm
	dxl_io.set_goal_position(dict(zip([8], [-15])))
	time.sleep(3)
			
	#Let it GO, let it gooOOO...
	dxl_io.set_goal_position(dict(zip([12], [-50])))
	time.sleep(4.5)
	
	#to not hit the object
	dxl_io.set_goal_position(dict(zip([8, 10], [10, 20])))
	time.sleep(2)
	dxl_io.set_goal_position(dict(zip([12], [50])))
	time.sleep(3)
	
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)
	print('Object moved to left')

def move_object_two_to_three(): #This one is correct and accurate
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)

	#Moving hand to position 2
	dxl_io.set_goal_position(dict(zip([3], [-10])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([4], [5])))
	time.sleep(2)
	dxl_io.set_goal_position(dict(zip([5, 6], [-30, 20])))
	time.sleep(3)
	#Open hand
	dxl_io.set_goal_position(dict(zip([7], [40])))  #this is correct
	time.sleep(4)
	dxl_io.set_goal_position(dict(zip([3, 4, 5], [20, -5, -40])))
	time.sleep(3)
	#Close hand
	dxl_io.set_goal_position(dict(zip([7], [-40])))
	time.sleep(4)
	#Move to postition 3
	dxl_io.set_goal_position(dict(zip([3, 4], [-10, 60])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([3, 5], [20, -25])))
	time.sleep(3)
	#Open hand
	dxl_io.set_goal_position(dict(zip([7], [50])))
	time.sleep(3)
	#Raise arm
	dxl_io.set_goal_position(dict(zip([3, 4], [-10, 45])))
	time.sleep(3)
				
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)
	print('Object moved to right')

def move_object_three_to_two(): #This one is good, ready for compound testing
	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)

	#Moving arm to position 3
	dxl_io.set_goal_position(dict(zip([3, 4], [-10, 70])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([6, 7], [10, 40])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([3, 4, 5], [25, 55, -30])))
	time.sleep(3)
	#Grabbing
	dxl_io.set_goal_position(dict(zip([7], [-40])))
	time.sleep(4)
	#Returning to position 2
	dxl_io.set_goal_position(dict(zip([3, 4, 5], [-20, -10, -55])))
	time.sleep(4)
	dxl_io.set_goal_position(dict(zip([3, 6], [27, 25])))
	time.sleep(4)
	#Open hand
	dxl_io.set_goal_position(dict(zip([7], [40])))
	time.sleep(3)
	#Raise arm
	dxl_io.set_goal_position(dict(zip([3, 4, 5], [-10, -20, -40])))
	time.sleep(3)
	dxl_io.set_goal_position(dict(zip([4, 7], [10, -30])))
	time.sleep(3)

	dxl_io.set_goal_position(dict(zip(ids, start_pose)))
	time.sleep(2)
	print("Object moved to center")

move_object_two_to_one()
move_object_one_to_two()
move_object_two_to_three()
move_object_three_to_two()
