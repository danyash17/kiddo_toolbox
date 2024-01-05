import sys
import os

from importmonkey import add_path
''' Export python module path '''

_i = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _i not in sys.path:
    add_path(_i)

from toolbox.print.banner import *
from toolbox.print.clprinter import *
from toolbox.util.iputils import *
from enum import Enum

'''
    Main module for port scanner
'''

tool_name = "KIDDO TOOLBOX PORTSCANNER"

print_horizontal_delimiter()
print_banner(tool_name)
print_horizontal_delimiter()

class TargetingType(Enum):
    SINGLE = 0,
    MULTIPLE = 1,
    RANGE = 2,
    SUBNET = 3

target_input = input("# Step 1: Specify a target IP\n"
                "# ex.:\n"
                "# 192.168.0.1 - single target\n"
                "# 192.168.0.1, 192.168.0.2 - multiple targets\n"
                "# 192.168.0.1-192.168.0.4 - range\n"
                "# 192.168.0.1/24 - subnet\n")

def define_targeting_type(target_input):
    if ',' in target_input:
        return TargetingType.MULTIPLE
    elif '-' in target_input:
        return TargetingType.RANGE
    elif '/' in target_input:
        return TargetingType.SUBNET
    else:
        return TargetingType.SINGLE

targeting_type = define_targeting_type(target_input)
target_list = list()
match targeting_type:
    case TargetingType.RANGE:
        target_list = get_range_ip_list(target_input)

