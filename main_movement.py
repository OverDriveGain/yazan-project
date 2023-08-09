##### this program is the main program for the whole task (Robot's movements, Camera, and results in GUI)
# from camera.save_and_load_image import take_photos_helper
# from classifier.predict import predict_image_list
# from GUI.start import start_grid_vis
# from utils import write_predict_result, read_predict_result
import time
import socket
import numpy as np
from operator import add
import robot_control as rc

#Should be something like this:
#
# Grab tool
# Move robot to cam
# Grab 1 image and save to output_images
# turn tool                                 ) repeat 7 times
# Grab 1 image and save to output_images    )
# predict image list ( If one of the pictures is schlecht, all are schlecht)
# put tool away
# calculate result
# show result in GUI
# Grab next tool
# and so on
# until all tools are processed
#
# And some example code:

# home position
home_position = [0.6, -0.163, 0.645, 2.27, -2.17, -0.1]

# pick positions
P1_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P2_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P3_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P4_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P5_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P6_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P7_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]
P8_position_pick = [0.617, -0.05, 0.231, 2.27, -1.94, -0.1]

pick_position_offset_approach   = [0.0, 0.0, 0.1, 0.0, 0.0, 0.0]  # offset for pick position approach (z axis)
pick_position_offset_leave      = [0.0, 0.0, 0.4, 0.0, 0.0, 0.0]     # offset for pick position leave (z axis)

# camera position
camera_position                 = [0.407, -0.466, 0.231, 1.4, -2.7, -0.181]
camera_position_offset_approach = [0.0, 0.0, 0.1, 0.0, 0.0, 0.0] # offset for camera position approach (z axis)
camera_position_offset_leave    = [0.0, 0.0, 0.4, 0.0, 0.0, 0.0] # offset for camera position approach (z axis)

# socket realtime connection
rt_socket = None

####### Socket settings:
HOST= "192.168.157.128"
PORT= 30003

# Define your new functions here. These are just placeholders and you'll need to implement them.

def close_gripper():
    f= open(".\close.script", "rb")
    l= f.read(1024)

    while (l):
        rt_socket.send(l)
        l= f.read(1024)
        time.sleep(0.001)

def open_gripper():
    f= open(".\open.script", "rb")
    l= f.read(1024)

    while (l):
        rt_socket.send(l)
        l= f.read(1024)
        time.sleep(0.001)

def go_to_home():
    rt_socket.send(("movej(get_inverse_kin(p" + str(home_position) + "), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

def grab_tool(position_pick : list):
    # Move to pick position with offset (approach)
    rt_socket.send(("movej(get_inverse_kin(pose_add(p" + str(position_pick) + ",p" + str(pick_position_offset_approach) + ")), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

    # Move to pick position
    rt_socket.send(("movel(p" + str(position_pick) + ", a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

    # Close gripper
    close_gripper()

    # Move up with offset (leave)
    rt_socket.send(("movel(pose_add(p" + str(position_pick) + ",p" + str(pick_position_offset_leave) + "), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

def move_robot_to_cam():
    # Move to camera position with offset (approach)
    rt_socket.send(("movej(get_inverse_kin(pose_add(p" + str(camera_position) + ",p" + str(camera_position_offset_approach) + ")), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

    # Move to camera position
    rt_socket.send(("movel(p" + str(camera_position) + ", a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

def move_robot_away_from_cam():
    # Move to camera position with offset (leave)
    rt_socket.send(("movel(pose_add(p" + str(camera_position) + ",p" + str(camera_position_offset_leave) + "), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

def find_tool_sensor(z_step: float, max_steps: int = 10):
    last_z_step = 0.0
    step = 0
    while True: 
        last_z_step += z_step
        if rc.get_digital_input(0) or step > max_steps:
            return True
        
        # Move down
        rt_socket.send(("movel(pose_add(p" + str(camera_position) + ",p"+str([0.0, 0.0, last_z_step, 0.0, 0.0, 0.0])  + "), a=2, v=2)" + "\n").encode('utf8'))
        rc.wait_robot_moving(rt_socket)
        rc.wait_robot_moving_done(rt_socket)
        step += 1      

def turn_tool(turn_angle : float):
    turn_position = rc.get_joint_positions()
    turn_position[5] += np.deg2rad(turn_angle) # convert to radians
    rt_socket.send(("movej(" + str(turn_position) + ", a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

def put_tool_away(position_pick : list):
    # Move to pick position with offset
    rt_socket.send(("movej(get_inverse_kin(pose_add(p" + str(position_pick) + ",p" + str(pick_position_offset_approach) + ")), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

    # Move to pick position
    rt_socket.send(("movel(p" + str(position_pick) + ", a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

    # Open gripper
    open_gripper()

    # Move up with offset (leave)
    rt_socket.send(("movel(pose_add(p" + str(position_pick) + ",p" + str(pick_position_offset_leave) + "), a=2, v=2)" + "\n").encode('utf8'))
    rc.wait_robot_moving(rt_socket)
    rc.wait_robot_moving_done(rt_socket)

# Take photo from camera
def take_photo():
    # output_images = take_photos_helper(8)
    # #output_images = ["classifier/testdataset/2208241448352.png"]
    # res = predict_image_list(output_images)
    # write_predict_result(res)
    # res_storage = read_predict_result()
    # start_grid_vis(res_storage)

    # Predict
    # store prediction
    # visualize in GUI
    pass

def calculate_result():

    pass  # Replace with code to calculate the result

# Assume we have a list of tools to process
tools = ['tool1', 'tool2', 'tool3', 'tool4', 'tool5', 'tool6', 'tool7', 'tool8']

def get_tool_position(tool_id):
    match tool_id:
        case 'tool1':
            return P1_position_pick
        case 'tool2':
            return P2_position_pick
        case 'tool3':
            return P3_position_pick
        case 'tool4':
            return P4_position_pick
        case 'tool5':
            return P5_position_pick
        case 'tool6':
            return P6_position_pick
        case 'tool7':
            return P7_position_pick
        case 'tool8':
            return P8_position_pick
        case _:
            return None

# main
if __name__ == '__main__':
    # Connect to robot
    rt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rt_socket.connect((HOST, PORT))
    time.sleep(0.1)

    # Go to home position
    go_to_home()

    # For each tool
    for tool in tools:
        # Get tool position
        tool_position = get_tool_position(tool)

        # Grab tool from pick position
        grab_tool(tool_position) #each tool should have coordinates ore previous defined moves assigned

        # Move robot to cam
        move_robot_to_cam()

        # Find tool sensor
        find_tool_sensor(0.01, 10)

        # Grab 1 image and save to output_images
        output_images = []
        turn_angle = 5     # in degrees
        for _ in range(8):
            take_photo() # take photo
            # output_images.append(take_photos_helper(1))  # Grab 1 image       
            turn_tool(turn_angle) # turn tool

        # Predict
        # res = predict_image_list(output_images)
        # write_predict_result(res)

        # move away from camera
        move_robot_away_from_cam()

        # retrun tool to pick position
        put_tool_away(tool_position)

        # store prediction
        # res_storage = read_predict_result()
        calculate_result()

    # After all tools are processed
    # start_grid_vis(res_storage)