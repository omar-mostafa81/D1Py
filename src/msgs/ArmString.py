# arm_string.py

from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

# Match the C++ type ::unitree_arm::msg::dds_::ArmString_
@dataclass
class ArmString_(IdlStruct, typename="unitree_arm::msg::dds_::ArmString_"):
    data_: str
