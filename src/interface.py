from unitree_sdk2py.core.channel import ChannelFactoryInitialize, ChannelSubscriber
from msgs.ArmString import ArmString_
from msgs.PubServoInfo import PubServoInfo_
import time

interface = "enx803f5dfb42af"

class D1Arm():
    def __init__(self):
        ChannelFactoryInitialize(0, interface)

        # Feedback data/subscribers
        self.latest_servo_data = None
        self.latest_arm_feedback = None
        self.sub_servo = ChannelSubscriber("current_servo_angle", PubServoInfo_)
        self.sub_arm = ChannelSubscriber("arm_Feedback", ArmString_)
        self.sub_servo.Init(self.handler_servo)
        self.sub_arm.Init(self.handler_arm_feedback, 10)

    ####### GET STATE ########
    def get_state(self):
        """
        returns the latest received data.
        """
        start_time = time.time()
        while time.time() - start_time < 1:
            if self.latest_servo_data and self.latest_arm_feedback:
                return self.latest_servo_data, self.latest_arm_feedback
            time.sleep(0.1) 

        return self.latest_servo_data, self.latest_arm_feedback

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
        # Update data
        self.latest_arm_feedback = {"armFeedback_data": msg.data_}

    ####### END GET STATE ########


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
