%YAML:1.0
---
# [pls dont change] The log level 
LogLevel: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 1. ] 

# [pls dont change] The threshold is applied to detect point cloud
Threshold: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 190. ] 

# [pls dont change] it's a switch for an algorithm in the process of computing stereo disparity 
Algorithm: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 1. ]

# UDP address for image transfer (e.g., 192.168.123.IpLastSegment)
IpLastSegment: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 15. ]  # Dit moet het laatste segment van het IP adres zijn van de nodige camera.

# DeviceNode
DeviceNode: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 1. ]  # Ik weet niet wat de nodes zijn van de cameras.

# fov (perspective 60~140) 
hFov: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 90. ]  # Adjust this value to change the field of view.

# image size ([1856,800] or [928,400])
FrameSize: !!opencv-matrix
   rows: 1
   cols: 2
   dt: d
   data: [ 1856., 800. ]  # Set this to the desired image resolution.

# rectified frame size
RectifyFrameSize: !!opencv-matrix
   rows: 1
   cols: 2
   dt: d
   data: [ 928., 800. ]  # Set this to the desired rectified image resolution.

# FrameRate, it gives the limitation for transmission rate (FPS)
FrameRate: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 3e+01 ]  # Change this to the desired frame rate (e.g., 30 FPS).

# 0 ori img - right 1 ori img - stereo 2 rect img - right 3 rect img - stereo -1 不传图
Transmode: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 2. ]  # Set the transmission mode (2 or 3).

# Transmission rate (FPS) in the UDP transmitting process. <= FrameRate
Transrate: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 3e+01 ]  # Set this to the desired transmission rate (should be <= FrameRate).

# [pls dont change] It's a switch in the distortion process of fisheye camera. 1 represents “Longitude and latitude expansion of fisheye camera”; 2 represents "Perspective distortion correction".
Depthmode: !!opencv-matrix
   rows: 1
   cols: 1
   dt: d
   data: [ 1. ]

# empty reserved IO
Reserved: !!opencv-matrix
   rows: 3
   cols: 3
   dt: d



What to Edit:
LogLevel, Threshold, Algorithm: Don't change it!

IpLastSegment: Modify this to match the last segment of the actual IP address you are using for image transfer.

DeviceNode: Set the device node number according to the device you are configuring.

hFov: Adjust the horizontal field of view as needed for your camera setup.

FrameSize: Set the desired image resolution for your camera.

RectifyFrameSize: Set the desired rectified image resolution.

FrameRate:Change the frame rate to the desired value, ensuring it matches the capabilities of your system.

Transmode: Set the transmission mode to 2 or 3, as required.

Transrate: Adjust the transmission rate, ensuring it is equal to or less than the frame rate.

Depthmode: Don't change!

Reserved: This section is reserved for future use and typically does not need to be edited.
