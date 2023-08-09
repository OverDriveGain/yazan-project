import socket
import time
import struct

# global variables
program_state = 0
robot_mode = 0
digital_inputs = [False, False, False, False, False, False, False, False]
digital_outputs = [False, False, False, False, False, False, False, False]

# joint positions
q_act_base:float = None
q_act_shoulder:float = None
q_act_elbow:float = None
q_act_wrist1: float = None
q_act_wrist2: float = None
q_act_wrist3:float = None

def get_robot_status(data: bytearray):
    global program_state, robot_mode, digital_inputs, digital_outputs, \
        q_act_base, q_act_shoulder, q_act_elbow, q_act_wrist1, q_act_wrist2, q_act_wrist3
    packlen = (struct.unpack('!i', data[0:4]))[0]
    if packlen == 1220: #v5.10 package
        data = data[4:]
        # program state
        program_state = (struct.unpack('!d', data[131*8:132*8]))[0]

        # robot mode
        robot_mode = (struct.unpack('!d', data[94*8:95*8]))[0]

        # digital inputs
        digital_inputs = double_to_8bit(struct.unpack('!d', data[85*8:86*8])[0])

        # digital outputs
        digital_outputs = double_to_8bit((struct.unpack('!d', data[130*8:131*8]))[0])

        # actual joint positions
        q_act_base     = (struct.unpack('!d', data[31*8:32*8]))[0]
        q_act_shoulder = (struct.unpack('!d', data[32*8:33*8]))[0]
        q_act_elbow    = (struct.unpack('!d', data[33*8:34*8]))[0]
        q_act_wrist1   = (struct.unpack('!d', data[34*8:35*8]))[0]
        q_act_wrist2   = (struct.unpack('!d', data[35*8:36*8]))[0]
        q_act_wrist3   = (struct.unpack('!d', data[36*8:37*8]))[0]

    elif packlen == 1140: #v5.9 package
        data = data[4:]

        # program state - 0 -? 1 - normal 2 - running
        program_state = (struct.unpack('!d', data[131*8:132*8]))[0]

        # robot mode
        robot_mode = (struct.unpack('!d', data[94*8:95*8]))[0]

        # digital inputs
        digital_inputs = double_to_8bit(struct.unpack('!d', data[85*8:86*8])[0])

        # digital outputs
        digital_outputs = double_to_8bit(struct.unpack('!d', data[130*8:131*8])[0])

        # actual joint positions
        q_act_base     = (struct.unpack('!d', data[31*8:32*8]))[0]
        q_act_shoulder = (struct.unpack('!d', data[32*8:33*8]))[0]
        q_act_elbow    = (struct.unpack('!d', data[33*8:34*8]))[0]
        q_act_wrist1   = (struct.unpack('!d', data[34*8:35*8]))[0]
        q_act_wrist2   = (struct.unpack('!d', data[35*8:36*8]))[0]
        q_act_wrist3   = (struct.unpack('!d', data[36*8:37*8]))[0]

def wait_robot_moving(rt_socket: socket.socket):
    while True:
        data = rt_socket.recv(4096)
        if len(data) > 0:
            get_robot_status(data)
            if get_robot_state() != 1:
                break
        time.sleep(0.001)   # sleep 1ms for sync with robot controller (1000Hz)

def wait_robot_moving_done(rt_socket: socket.socket):
    while True:
        data = rt_socket.recv(4096)
        if len(data) > 0:
            get_robot_status(data)
            if get_robot_state() == 1:
                break
        time.sleep(0.001)   # sleep 1ms for sync with robot controller (1000Hz)

def get_robot_state():
    global program_state
    return program_state

def get_robot_mode():
    global robot_mode
    return robot_mode

def get_digital_inputs():
    global digital_inputs
    return digital_inputs

def get_digital_input(index: int) -> bool:
    global digital_inputs
    return digital_inputs[index]

def get_digital_outputs():
    global digital_outputs
    return digital_outputs

def get_digital_output(index: int) -> bool:
    global digital_outputs
    return digital_outputs[index]

def get_joint_positions():
    global q_act_base, q_act_shoulder, q_act_elbow, q_act_wrist1, q_act_wrist2, q_act_wrist3
    return [q_act_base, q_act_shoulder, q_act_elbow, q_act_wrist1, q_act_wrist2, q_act_wrist3]

def double_to_8bit(d):
    binary_str = bin(int(d))[2:].zfill(8)
    binary_array = [bool(int(bit)) for bit in binary_str]
    return binary_array[::-1]