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
    tcpRequest = IP(dst=ip) / TCP(dport=port, flags="S")
    tcpResponse = sr1(tcpRequest, timeout=1, verbose=0)
    try:
        if tcpResponse.getlayer(TCP).flags == "SA":
            return True
    except AttributeError:
        return False
