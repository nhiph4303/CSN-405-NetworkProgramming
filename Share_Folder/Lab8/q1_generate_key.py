import rsa

public_key, private_key = rsa.newkeys(2048)

with open("client_private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))

with open("client_public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

print("RSA key pair generated successfully")