from scapy.all import *
from scapy.layers.inet import TCP, IP, ICMP


def is_host_up(ip):
    '''
        Pings host to ensure it is up
    '''
    ping = IP(dst=ip) / ICMP()
    res = sr1(ping, timeout=1, verbose=0)
    if res == None:
        return False
    else:
        return True


def is_port_opened_syn(ip, port):
    '''
        Check if port is opened using stealth scan technique (SYN)
    '''
    tcp_request = IP(dst=ip) / TCP(dport=port, flags="S")
    tcp_response = sr1(tcp_request, timeout=1, verbose=0)
    try:
        if tcp_response.getlayer(TCP).flags == "SA":
            return True
    except AttributeError:
        return False
