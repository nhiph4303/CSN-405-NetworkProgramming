import ipaddress

def validate_ip(ip: str) -> str:
    try:
        ipaddress.IPv4Address(ip)
        return ip
    except ipaddress.AddressValueError:
        raise ValueError(f"Invalid IP address: '{ip}'.")

def validate_port(port) -> int:
    try:
        port_num = int(port)
    except ValueError:
        raise ValueError("Port must be a number.")
        
    if not (1 <= port_num <= 65535):
        raise ValueError("Port must be between 1 and 65535.")
    return port_num

def validate_role(role: str) -> str:
    role_cleaned = str(role).strip().lower()
    if role_cleaned not in ('client', 'server'):
        raise ValueError("Role must be either 'client' or 'server'.")
    return role_cleaned

def validate_protocol(protocol: str) -> str:
    protocol_cleaned = str(protocol).strip().upper()
    if protocol_cleaned not in ('TCP', 'UDP'):
        raise ValueError("Protocol must be 'TCP' or 'UDP'.")
    return protocol_cleaned