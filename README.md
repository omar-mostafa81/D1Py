
# D1Py
Python Interface for the Unitree D1 Arm

## Dependencies

**unitree_sdk2_python**

Unitree Python SDK: [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python)

**d1py_sdk**
The `d1py_sdk` is part of this project. It was implemented as a python version of [d1_sdk](https://unitree-firmware.oss-cn-hangzhou.aliyuncs.com/tool/d1_sdk.zip) by Unitree.

## How to Use

 1.  **Clone the repository**:    
 ```shell
   git clone https://github.com/omar-mostafa81/D1Py
 ```    
 2.  **Install the package**: 
 ```shell
 cd D1Py 
 pip install -e .
 ```
 
3.  **Import and use `D1Arm`**:
   ```python
   from d1py.interface import D1Arm
   robot = D1Arm()
   ```

**Available Functions:**
`set_joint(id, angle, delay=0)`: Move a single joint to `angle` (°) after `delay` ms.

`set_all_joints(angles, mode=0)`: Move all joints; `angles` must be a 7-element list. `mode`: `0` = 10 Hz smoothing, `1` = trajectory smoothing.

`force_discharge_joint(id, mode)`: Enable/disable force on one joint. `mode`: `0` = release torque, `1` = enable.

`force_discharge_all(mode)`:  Enable/disable force on all joints.

`switch_motor_power(mode)`: Master power: `0` = off, `1` = on.

`reset()`: Return arm posture to zero (predefined home).

`get_joint_state()`: Latest servo angle feedback (dict of joint data).

`get_arm_status_feedback()`: Latest overall arm enable/power/error status.

`get_motor_online_status()`: Per-motor online status (1 = OK, 0 = fault).
 
`get_recv_status_feedback()`: Flag showing if last command was received (`1` = success).

`get_exec_status_feedback()`: Flag showing if last command executed (`1` = success).

`get_combined_arm_feedback()`: returns all feedback fields in one dict.

`close()`: Cleanly close all subscribers/publishers.