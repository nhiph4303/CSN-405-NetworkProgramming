import uuid 
from app.utils.validator import validate_ip, validate_port, validate_role, validate_protocol
class NetworkNode() :
    def __init__(self, ip, port, role, protocol):
       
        # Kiểm tra dữ liệu hợp lệ - nếu sai sẽ raise Exception
        validate_ip(ip)
        validate_port(port)
        validate_role(role)
        validate_protocol(protocol)

        # Nếu hợp lệ thì lưu vào object
        self.node_id = str(uuid.uuid4()) #automatically generated

        self.ip = ip
        self.port = port
        self.role = role
        self.protocol = protocol

        