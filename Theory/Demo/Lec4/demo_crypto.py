from cryptography.fernet import Fernet

key = Fernet.generate_key()

print(key)

message = b"Hello, World!"

f = Fernet(key)
encrypted_message = f.encrypt(message)

print(f"Original message: {message}")
print(f"Encrypted message: {encrypted_message}")

decrypted_message = f.decrypt(encrypted_message)
print(f"Decrypted message: {decrypted_message}")

if decrypted_message == message:
    print("Decryption successful!")
