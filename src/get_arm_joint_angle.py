#!/usr/bin/env python3

import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize

from msgs.PubServoInfo import PubServoInfo_
from msgs.ArmString import ArmString_

def handler_servo(msg: PubServoInfo_):
    """
    Callback for current_servo_angle topic.
    Prints all seven joint angles.
    """
    # print(
    #     f"servo0_data: {msg.servo0_data_}, "
    #     f"servo1_data: {msg.servo1_data_}, "
    #     f"servo2_data: {msg.servo2_data_}, "
    #     f"servo3_data: {msg.servo3_data_}, "
    #     f"servo4_data: {msg.servo4_data_}, "
    #     f"servo5_data: {msg.servo5_data_}, "
    #     f"servo6_data: {msg.servo6_data_}"
    # )

def handler_arm_feedback(msg: ArmString_):
    """
    Callback for arm_Feedback topic.
    Prints the feedback string.
    """
    print(f"armFeedback_data: {msg.data_}")

def main():
    # init DDS (optionally pass domain ID or XML config)
    if len(sys.argv) > 1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)
    
    # # subscribe to joint angles
    sub_servo = ChannelSubscriber("current_servo_angle", PubServoInfo_)
    sub_servo.Init(handler_servo)

    # subscribe to string feedback
    sub_arm = ChannelSubscriber("arm_Feedback", ArmString_)
    sub_arm.Init(handler_arm_feedback, 10)

    try:
        # keep the script alive, callbacks fire on incoming messages
        while True:
            print("waiting")
            time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        sub_servo.Close()
        sub_arm.Close()

if __name__ == "__main__":
    main()
