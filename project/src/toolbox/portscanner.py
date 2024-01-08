import sys
import os
import socket

from importmonkey import add_path

''' Export python module path '''

_i = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _i not in sys.path:
    add_path(_i)

from toolbox.print.banner import *
from toolbox.print.clprinter import *
from toolbox.util.iputils import *
from toolbox.util.portutils import *
from toolbox.scan.scanner import *
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


class PortScanType(Enum):
    SINGLE = 0,
    MULTIPLE = 1,
    RANGE = 2


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


def define_porting_type(port_input):
    if ',' in port_input:
        return PortScanType.MULTIPLE
    if '-' in port_input:
        return PortScanType.RANGE
    else:
        return PortScanType.SINGLE


def exec_syn_scan(target_list, port_list):
    print("STARTING SCANNING IN STEALTH MODE (TCP SYN)")
    for target in target_list:
        if not is_host_up(target):
            print_hose_is_down(target)
            continue
        print_scan_target(target)
        for port in port_list:
            if is_port_opened_syn(target, port):
                print_detected_opened_port(target, port)


targeting_type = define_targeting_type(target_input)
target_list = list()
match targeting_type:
    case TargetingType.RANGE:
        target_list = get_range_ip_list(target_input)
    case TargetingType.MULTIPLE:
        target_list = get_multiple_ip_list(target_input)
    case TargetingType.SUBNET:
        target_list = get_subnet_ip_list(target_input)
    case TargetingType.SINGLE:
        target_list.append(target_input.strip())

print_horizontal_delimiter()
port_input = input("# Step 2: Specify ports to be scanned\n"
                   "# ex.:\n"
                   "# 80 - single target\n"
                   "# 80, 53 - multiple targets\n"
                   "# 53-80 - range\n")
porting_type = define_porting_type(port_input)
port_list = list()
match porting_type:
    case PortScanType.RANGE:
        port_list = get_range_ports_list(port_input)
    case PortScanType.MULTIPLE:
        port_list = get_multiple_ports_list(port_input)
    case PortScanType.SINGLE:
        port_list.append(port_input.strip())
print_horizontal_delimiter()
print_radar()
try:
    exec_syn_scan(target_list, port_list)
except PermissionError as pe:
    if pe.errno == 1:
        print("\n Root privileges are needed for raw sockets, please re-run as root\n")
print_horizontal_delimiter()
print("Step 3: ???")
print("Step 4: PROFIT!")
