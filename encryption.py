from cryptography.fernet import Fernet

class EncryptionManager:
    def __init__(self):
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):
        try:
            with open('encryption_key.key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('encryption_key.key', 'wb') as key_file:
                key_file.write(key)
            return key

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data).decode()