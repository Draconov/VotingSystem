from cryptography.fernet import Fernet

def create_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key created successfully.")

if __name__ == "__main__":
    create_key()