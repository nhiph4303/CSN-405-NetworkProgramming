import os

def generate_aes_key():
    key = os.urandom(32)
    
    with open("aes.key", "wb") as f:
        f.write(key)
        
    print("AES key (256-bit) generated successfully and saved to 'aes.key'")

if __name__ == "__main__":
    generate_aes_key()
