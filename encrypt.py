import sys
import json
from cryptography.fernet import Fernet
from dotenv import dotenv_values
from getpass import getpass

def main():
    print("Please input your password")
    password=getpass()
    
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encPassword = fernet.encrypt(password.encode())

    #Write key to .env
    with open(".env", "w") as f:
            f.write(f"key={key.decode()}")
    #Store encrypted password inside config.json
    with open("config.json") as json_file:
        json_decoded = json.load(json_file)

    json_decoded['password'] = encPassword.decode()

    with open("config.json", 'w') as json_file:
        json.dump(json_decoded, json_file)

    
    print("Password has been encrypted and stored inside config.json.")


if __name__=="__main__":
    main()