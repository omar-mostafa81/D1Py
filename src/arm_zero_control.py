# arm_zero_control.py

from unitree_sdk2py.core.channel import ChannelPublisher, ChannelFactoryInitialize
from msgs.ArmString import ArmString_

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ChannelFactoryInitialize(0, sys.argv[1])
    else:
        ChannelFactoryInitialize(0)

    pub = ChannelPublisher("rt/arm_Command", ArmString_)
    pub.Init()

    msg = ArmString_(data_='{\"seq\":4,\"address\":1,\"funcode\":7}')
    success = pub.Write(msg, 0.5)

    if success:
        print("msg sent")
    else:
        print("Waiting for subscriber or publish failed")

    pub.Close()
