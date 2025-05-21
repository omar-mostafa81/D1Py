# set_servo_angle.py

from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

# Match the C++ type ::unitree_arm::msg::dds_::SetServoAngle_
@dataclass
class SetServoAngle_(IdlStruct, typename="unitree_arm::msg::dds_::SetServoAngle_"):
    seq_: int        # int32_t
    id_: int         # uint8_t (use int for compatibility)
    angle_: float    # float
    delay_ms_: int   
