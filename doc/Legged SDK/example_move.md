#!/usr/bin/python

import sys
import time
import math

sys.path.append('../lib/python/amd64')
import robot_interface as sdk


if __name__ == '__main__':

    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff

    udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

    motiontime = 0
    while True:
        time.sleep(0.002)
        motiontime = motiontime + 1

        udp.Recv()
        udp.GetRecv(state)
        
        # print(motiontime)
        # print(state.imu.rpy[0])
        # print(motiontime, state.motorState[0].q, state.motorState[1].q, state.motorState[2].q)
        # print(state.imu.rpy[0])

#Sets robot in idle mode.

        cmd.mode = 0      # 0:idle, default stand      1:forced stand     2:walk continuously
        cmd.gaitType = 0
        cmd.speedLevel = 0
        cmd.footRaiseHeight = 0
        cmd.bodyHeight = 0
        cmd.euler = [0, 0, 0]
        cmd.velocity = [0, 0]
        cmd.yawSpeed = 0.0
        cmd.reserve = 0

        # cmd.mode = 2
        # cmd.gaitType = 1
        # # cmd.position = [1, 0]
        # # cmd.position[0] = 2
        # cmd.velocity = [-0.2, 0] # -1  ~ +1
        # cmd.yawSpeed = 0
        # cmd.bodyHeight = 0.1

#This defines a sequence of movements

        if(motiontime > 0 and motiontime < 1000):
            cmd.mode = 1
            cmd.euler = [-0.3, 0, 0]
        
        if(motiontime > 1000 and motiontime < 2000):
            cmd.mode = 1
            cmd.euler = [0.3, 0, 0]
        
        if(motiontime > 2000 and motiontime < 3000):
            cmd.mode = 1
            cmd.euler = [0, -0.2, 0]
        
        if(motiontime > 3000 and motiontime < 4000):
            cmd.mode = 1
            cmd.euler = [0, 0.2, 0]
        
        if(motiontime > 4000 and motiontime < 5000):
            cmd.mode = 1
            cmd.euler = [0, 0, -0.2]
        
        if(motiontime > 5000 and motiontime < 6000):
            cmd.mode = 1
            cmd.euler = [0.2, 0, 0]
        
        if(motiontime > 6000 and motiontime < 7000):
            cmd.mode = 1
            cmd.bodyHeight = -0.2
        
        if(motiontime > 7000 and motiontime < 8000):
            cmd.mode = 1
            cmd.bodyHeight = 0.1
        
        if(motiontime > 8000 and motiontime < 9000):
            cmd.mode = 1
            cmd.bodyHeight = 0.0
        
        if(motiontime > 9000 and motiontime < 11000):
            cmd.mode = 5
        
        if(motiontime > 11000 and motiontime < 13000):
            cmd.mode = 6
        
        if(motiontime > 13000 and motiontime < 14000):
            cmd.mode = 0
        
        if(motiontime > 14000 and motiontime < 18000):
            cmd.mode = 2
            cmd.gaitType = 2  #walking type
            cmd.velocity = [0.4, 0] # -1  ~ +1  #speed
            cmd.yawSpeed = 2  #Turning speed
            cmd.footRaiseHeight = 0.1  #height that foots are raised
            # printf("walk\n")
        
        if(motiontime > 18000 and motiontime < 20000):
            cmd.mode = 0
            cmd.velocity = [0, 0]
        
        if(motiontime > 20000 and motiontime < 24000):
            cmd.mode = 2
            cmd.gaitType = 1
            cmd.velocity = [0.2, 0] # -1  ~ +1
            cmd.bodyHeight = 0.1
            # printf("walk\n")
            

        udp.SetSend(cmd)
        udp.Send()


#This script makes the Unitree Go1 perform a sequence of actions:
0 to 1000 ms: The robot forces a stand with a slight forward tilt.
1000 to 2000 ms: The robot forces a stand with a slight backward tilt.
2000 to 3000 ms: The robot forces a stand with a left tilt.
3000 to 4000 ms: The robot forces a stand with a right tilt.
4000 to 5000 ms: The robot forces a stand with a slight roll to the left.
5000 to 6000 ms: The robot forces a stand with a slight roll to the right.
6000 to 7000 ms: The robot lowers its body.
7000 to 8000 ms: The robot raises its body slightly.
8000 to 9000 ms: The robot returns to a normal body height.
9000 to 11000 ms: The robot performs mode 5 (likely a predefined behavior, e.g., sitting).
11000 to 13000 ms: The robot performs mode 6 (another predefined behavior).
13000 to 14000 ms: The robot goes back to idle.
14000 to 18000 ms: The robot walks with a trotting gait, moving forward at 0.4 m/s and turning with a yaw speed of 2 rad/s.
18000 to 20000 ms: The robot goes idle and stops moving.
20000 to 24000 ms: The robot walks with a walking gait, moving forward at 0.2 m/s and slightly raising its body height.
