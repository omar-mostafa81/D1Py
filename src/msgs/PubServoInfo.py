from dataclasses import dataclass
from cyclonedds.idl import IdlStruct
from cyclonedds.idl.types import float32

# Match the C++ type ::unitree_arm::msg::dds_::PubServoInfo_
@dataclass
class PubServoInfo_(IdlStruct, typename="unitree_arm::msg::dds_::PubServoInfo_"):
    servo0_data_: float32
    servo1_data_: float32
    servo2_data_: float32
    servo3_data_: float32
    servo4_data_: float32
    servo5_data_: float32
    servo6_data_: float32

