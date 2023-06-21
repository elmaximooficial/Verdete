from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
unpad = lambda s: s[0:-ord(s[-1])]

class User:
    username : str
    password : str
    password_tag : str

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __init__(self):
        print('hello')

    def load_user(pass_manager, username, password):
        try:
            user = User()
            with open(f'{username}.dat', 'rb') as file:
                pass_file, tag = file.read().split(b'\n')
                if password == pass_manager.decrypt_pwd(password=pass_file, tag=tag).decode():
                    user.username = username
                    user.password = password
                    user.tag = file.read().split(b'\n')[1]
                else:
                    print(f'Wrong password for user {username}')
        except FileNotFoundError:
            print(f'{username} was not found, if you didn\'t set it up, run the program with --gen-password password~username')

class PasswordManager:
    key : str
    nonce : str
    cipher : AES

    def __init__(self, key, nonce, cipher):
        self.key = key
        self.nonce = nonce
        self.cipher = cipher
    def __init__(self):
        print('hello')

    def gen_key():
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        try:
            with open('key.pem', 'wb') as file:
                file.write(key + b'\n' + nonce)
        except FileExistsError:
            os.remove('key.pem')
            PasswordManager.gen_key()

    def load_key():
        try:
            with open('key.pem', 'rb') as file:
                pass_manager = PasswordManager()
                key, nonce = file.read().split(b'\n')
                pass_manager.key = key
                pass_manager.cipher = AES.new(pass_manager.key, AES.MODE_EAX)
                return pass_manager
        except FileNotFoundError:
            PasswordManager.gen_key()
            PasswordManager.load_key()

    def gen_encrypted_pwd(self, password : str, username : str):
        if self.cipher != None:
            ciphertext, tag = self.cipher.encrypt_and_digest(password.encode())
            print("Hello from gen_encrypted_password")
            print(ciphertext + b'\n' + tag)
            with open(f'{username}.dat', 'wb') as file:
                file.write(ciphertext + b'\n' + tag)
        else:
            print("Bye from gen_encrypted_password")
            self.load_key()
            self.gen_encrypted_pwd(password, username)

    def decrypt_pwd(self, password, tag):
        if self.key != None and self.cipher.nonce != None:
            plaintext = self.cipher.decrypt(password)
            try:
                self.cipher.verify(tag)
                print("Everything ok")
                return plaintext
            except ValueError as e:
                print(e)
        else:
            self.load_key()
            self.decrypt_pwd(password, tag)