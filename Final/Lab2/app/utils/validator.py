import ipaddress

#The IP address must be valid
def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)  
    except ValueError:
        raise ValueError(f"Invalid IP address: {ip}")

#The port must be between 1 and 65535
def validate_port(port):
    if not (1 <= port <= 65535):
        raise ValueError("Port must be between 1 and 65535")

#The role must only accept either client or server
def validate_role(role):
    if role not in ["client", "server"]:
        raise ValueError("Role must be 'client' or 'server'")

#Protocol (only TCP or UDP)
def validate_protocol(protocol):
    if protocol not in ["tcp", "udp"]:
        raise ValueError("Protocol must be 'tcp' or 'udp'")
