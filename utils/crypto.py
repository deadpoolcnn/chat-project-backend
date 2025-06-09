# 加解密相关工具函数（RSA/AES/签名等）
def generate_rsa_keypair():
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    return {'private_key': private_key, 'public_key': public_key}

def encrypt_with_rsa(public_key, data):
    pass

def decrypt_with_rsa(private_key, encrypted_data):
    pass

def generate_aes_key():
    pass

def encrypt_with_aes(aes_key, plaintext):
    pass

def decrypt_with_aes(aes_key, iv, ciphertext):
    pass

def sign_message(private_key, message):
    pass

def verify_signature(public_key, message, signature):
    pass
