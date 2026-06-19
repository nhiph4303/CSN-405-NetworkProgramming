from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
print(private_key)

public_key = private_key.public_key()
print(public_key)

import pdb; pdb.set_trace()
