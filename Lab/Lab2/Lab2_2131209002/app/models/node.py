import uuid
from app.utils.validator import validate_ip, validate_port, validate_role, validate_protocol

class NetworkNode:
    def __init__(self, ip: str, port: int, role: str, protocol: str):
        self.node_id = str(uuid.uuid4())

        self.ip = validate_ip(ip)
        self.port = validate_port(port)
        self.role = validate_role(role)
        self.protocol = validate_protocol(protocol)

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "ip": self.ip,
            "port": self.port,
            "role": self.role,
            "protocol": self.protocol
        }