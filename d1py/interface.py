from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber, ChannelPublisher
from .d1py_sdk.msgs.ArmString import ArmString_
from .d1py_sdk.msgs.PubServoInfo import PubServoInfo_
import time
import sys
import json

interface = "enx803f5dfb42af"

class D1Arm():
    def __init__(self):
        if len(sys.argv) > 1:
            ChannelFactoryInitialize(0, sys.argv[1])
        else:
            ChannelFactoryInitialize(0, interface)

        # Feedback data/subscribers
        self.latest_servo_data = None
        self.arm_status_feedback = None          # from address=2, funcode=3
        self.motor_online_status = None          # from address=2, funcode=4
        self.recv_status_feedback = None         # from address=3, funcode=1
        self.exec_status_feedback = None         # from address=3, funcode=2
        self.latest_arm_feedback = None

        self.sub_servo = ChannelSubscriber("current_servo_angle", PubServoInfo_)
        self.sub_arm = ChannelSubscriber("arm_Feedback", ArmString_)
        self.sub_servo.Init(self.handler_servo)
        self.sub_arm.Init(self.handler_arm_feedback, 10)

        # Control data
        self.CMD_TOPIC = "rt/arm_Command"

    ####### GET STATE Functions ########
    def get_joint_state(self):
        """
        returns the latest received joint state data.
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.latest_servo_data:
                return self.latest_servo_data
            time.sleep(0.1) 

        return self.latest_servo_data
    
    def get_arm_status_feedback(self):
        """
        returns the latest received arm state data.
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.arm_status_feedback:
                return self.arm_status_feedback
            time.sleep(0.1) 

        return self.arm_status_feedback

    def get_motor_online_status(self):
        """
        returns the latest received motor online state data.
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.motor_online_status:
                return self.motor_online_status
            time.sleep(0.1) 
        return self.motor_online_status

    def get_recv_status_feedback(self):
        """
        returns the received command flag 
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.recv_status_feedback:
                return self.recv_status_feedback
            time.sleep(0.1) 

        return self.recv_status_feedback

    def get_exec_status_feedback(self):
        """
        returns the executed command flag 
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.exec_status_feedback:
                return self.exec_status_feedback
            time.sleep(0.1) 
        return self.exec_status_feedback

    # Combined feedback getter
    def get_combined_arm_feedback(self):
        """
        returns all feedback data combined 
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.latest_arm_feedback:
                return self.latest_arm_feedback
            time.sleep(0.1) 
        return self.latest_arm_feedback

    def handler_servo(self, msg: PubServoInfo_):
        # Update data
        self.latest_servo_data = {
            "servo0_data": msg.servo0_data_,
            "servo1_data": msg.servo1_data_,
            "servo2_data": msg.servo2_data_,
            "servo3_data": msg.servo3_data_,
            "servo4_data": msg.servo4_data_,
            "servo5_data": msg.servo5_data_,
            "servo6_data": msg.servo6_data_,
        }

    def handler_arm_feedback(self, msg: ArmString_):
        """
        "address":2,"funcode":3 -> Robotic arm status feedback 
        "address":2,"funcode":4 -> Online status detection of mechanical arm motor (if motor is faulty: 0, else: 1)
        "address":3,"funcode":1 -> reception is successful: 1, else 0
        "address":3,"funcode":2 -> execution succeeds: 1, else: 0
        """
        data_str = msg.data_  # JSON string
        data = json.loads(data_str)  # convert to dict
        address = data.get("address")
        funcode = data.get("funcode")
        payload = data.get("data")

        if address == 2 and funcode == 3:
            # Robotic arm status feedback
            self.arm_status_feedback = payload
            self.latest_arm_feedback["arm_status"] = payload

        elif address == 2 and funcode == 4:
            # Online status detection of mechanical arm motor
            self.motor_online_status = payload
            self.latest_arm_feedback["motor_online_status"] = payload

        elif address == 3 and funcode == 1:
            # Reception success feedback
            self.recv_status_feedback = payload
            self.latest_arm_feedback["recv_status"] = payload

        elif address == 3 and funcode == 2:
            # Command execution feedback
            self.exec_status_feedback = payload
            self.latest_arm_feedback["exec_status"] = payload

    ####### Control Functions ########
    def reset(self):
        """ robotic arm posture returns to zero
        """
        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_='{"seq":4,"address":1,"funcode":7}')
        success = pub.Write(msg, 0.5)
        if success:
            print("reset command sent")
        else:
            print("waiting for subscriber")

        pub.Close()
    
    def set_joint(self, id, angle, delay = 0.0):
        """ Sets the specified joint to the specified angle
        "id": joint number 
        "angle": joint target angle
        "delay_ms": execution time
        """
        if id not in range(7):
            raise ValueError("ID must be int from 0 to 6")
        
        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_=f'{{"seq":4,"address":1,"funcode":1,"data":{{"id":{id},"angle":{angle},"delay_ms":{delay}}}}}')
        success = pub.Write(msg, 0.5)
        if success:
            print(f"Set joint command sent for joint {id}.")
        else:
            print("waiting for subscriber")

        pub.Close()
    
    def set_all_joints(self, angles, mode = 0):
        """ Sets all robotic arm joint to the specified angles
        "mode": mode 0 is the small smoothing of 10Hz data, and mode 1 is the large smoothing of trajectory use
        "angles": list of desired angles
        """
        if len(angles) != 7:
            raise ValueError("Must provide exactly 7 joint angles")
        if mode not in [0, 1]:
            raise ValueError("Mode must be 0 (small smoothing of 10Hz data) or 1 (large smoothing)")
    
        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_=f'{{"seq":4,"address":1,"funcode":2,"data":{{"mode":{mode},"angle0":{angles[0]},"angle1":{angles[1]},"angle2":{angles[2]},"angle3":{angles[3]},"angle4":{angles[4]},"angle5":{angles[5]},"angle6":{angles[6]}}}}}')
        success = pub.Write(msg, 0.5)
        if success:
            print("Set joint command sent for all joints")
        else:
            print("waiting for subscriber")

        pub.Close()
    
    def force_discharge_joint(self, id, mode):
        """ Enable/force discharge control of a single manipulator joint motor.
        Args:
            id: joint id
            mode: 0 = release force, 1 = enable force discharge
        """
        if mode not in [0, 1]:
            raise ValueError("Mode must be 0 (release force) or 1 (enable force discharge)")
        if id not in range(7):
            raise ValueError("ID must be int from 0 to 6")
        
        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_=f'{{"seq":4,"address":1,"funcode":4,"data":{{"id":{id},"mode":{mode}}}}}')
        success = pub.Write(msg, 0.5)
        if success:
            print(f"Force discharge command sent for joint {id} with mode {mode}")
        else:
            print("waiting for subscriber")

        pub.Close()


    def force_discharge_all(self, mode):
        """ Enable/force discharge control of all mechanical arm joint motors.
        Args:
            mode: 0 = release force, 1 = enable force discharge
        """
        if mode not in [0, 1]:
            raise ValueError("Mode must be 0 (release force) or 1 (enable force discharge)")
        
        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_=f'{{"seq":4,"address":1,"funcode":5,"data":{{"mode":{mode}}}}}')
        success = pub.Write(msg, 0.5)
        if success:
            print(f"Force discharge command sent for all joints with mode {mode}")
        else:
            print("waiting for subscriber")

        pub.Close()
    
    ###### GENERAL #######
    def switch_motor_power(self, mode):
        """ Power supply switch of the mechanical arm motor
        Args:
            mode (int): 0 = power off, 1 = power on
        """
        if mode not in [0, 1]:
            raise ValueError("Mode must be 0 (off) or 1 (on)")

        pub = ChannelPublisher(self.CMD_TOPIC, ArmString_)
        pub.Init()

        msg = ArmString_(data_=f'{{"seq":4,"address":1,"funcode":6,"data":{{"power":{mode}}}}}')

        success = pub.Write(msg, 0.5)
        if success:
            print(f"Power supply {'on' if mode == 1 else 'off'} command sent")
        else:
            print("waiting for subscriber")

        pub.Close()

    def close(self):
        self.sub_servo.Close()
        self.sub_arm.Close()

if __name__ == "__main__":
    robot = D1Arm()
    try:
        servo_data, arm_feedback = robot.get_state()
        print("Servo data:", servo_data)
        print("Arm feedback:", arm_feedback)
    finally:
        robot.close()
