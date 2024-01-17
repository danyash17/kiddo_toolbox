import psutil
import socket

OCT_MIN = 0
OCT_MAX = 255


class Ip:

    def __init__(self, *args):
        if len(args) == 1:
            self.first, self.second, self.third, self.fourth = args[0]
        else:
            self.first, self.second, self.third, self.fourth = args

    def __str__(self):
        return f"{self.first}.{self.second}.{self.third}.{self.fourth}"

    @classmethod
    def from_string(cls, ip_string):
        first, second, third, fourth = map(int, ip_string.split('.'))
        return cls(first, second, third, fourth)

    @classmethod
    def from_int_list(cls, int_list):
        first, second, third, fourth = int_list
        return cls(first, second, third, fourth)

    def to_int_list(self):
        return self.first, self.second, self.third, self.fourth

    def increment(self):
        if self.fourth < OCT_MAX:
            self.fourth += 1
        elif self.third < OCT_MAX:
            self.third += 1
            self.fourth = OCT_MIN
        elif self.second < OCT_MAX:
            self.second += 1
            self.third = OCT_MIN
            self.fourth = OCT_MIN
        elif self.first < OCT_MAX:
            self.first += 1
            self.second = OCT_MIN
            self.third = OCT_MIN
            self.fourth = OCT_MIN
        else:
            raise ValueError("IP address out of range")

        return self


def first_non_zero_index(lst):
    for i, val in enumerate(lst):
        if val != 0:
            return i
    return -1  # If all elements are zero


def get_range_ip_list(str_range):
    '''
        Get IP list from range string representation (ex. "192.168.0.1-192.168.0.3" ->
        [192.168.0.1", "192.168.0.2", "192.168.0.3"])
    '''
    # First, decompose string representation of IPs to int lists '''
    borders = str_range.strip().split('-')
    from_octets = list(map(int, borders[0].split('.')))
    to_octets = list(map(int, borders[1].split('.')))
    if len(from_octets) != len(to_octets):
        raise ValueError("Wrong octets number")
    range_ip_list = list()
    while (True):
        # Iterate within range until the upper border is reached
        if from_octets != to_octets:
            ip = Ip(from_octets)
            range_ip_list.append(ip.__str__())
            ip = ip.increment()
            from_octets = list(ip.to_int_list())
        else:
            return range_ip_list


def get_multiple_ip_list(str_multiple):
    '''
        Get IP list from multiple string representation (ex. "192.168.0.1, 192.168.0.3" ->
        [192.168.0.1", "192.168.0.3"])
    '''
    return str_multiple.strip().split(',')


def get_subnet_ip_list(str_subnet):
    '''
       Get IP list from subnet string representation (ex. "192.168.0.1/24" ->
       [192.168.0.1", "192.168.0.2", ... , "192.168.0.255"])
    '''
    # Parse the subnet string
    ip_str, mask_str = str_subnet.split('/')
    ip_parts = list(map(int, ip_str.split('.')))
    mask_bits = int(mask_str)

    # Calculate the subnet mask
    mask = 0xffffffff << (32 - mask_bits)
    mask_parts = [(mask >> i) & 0xff for i in (24, 16, 8, 0)]

    # Calculate the network address and broadcast address
    net_addr = [ip_parts[i] & mask_parts[i] for i in range(4)]
    bcast_addr = [(net_addr[i] | ~mask_parts[i]) & 0xff for i in range(4)]

    # Generate the list of IP addresses in the subnet
    ip_list = []
    for i in range(net_addr[3] + 1, bcast_addr[3]):
        ip = '{}.{}.{}.{}'.format(net_addr[0], net_addr[1], net_addr[2], i)
        ip_list.append(ip)

    return ip_list

def get_interfaces_ipv4_dict():
    interfaces = psutil.net_if_addrs()
    return {interface: next(
        (addr.address for addr in interfaces[interface] if addr.family == socket.AF_INET and addr.address), None) for
            interface in interfaces}