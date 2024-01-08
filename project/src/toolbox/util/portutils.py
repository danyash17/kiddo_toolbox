def get_multiple_ports_list(port_input):
    return port_input.strip().split(',')

def get_range_ports_list(port_input):
    from_port, to_port = port_input.strip().split('-')
    return list(range(from_port, to_port + 1))