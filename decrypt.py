import json
from cryptography.fernet import Fernet
from dotenv import dotenv_values


def decryptPassword(password):
    try:
        #read key from .env
        config = dotenv_values(".env")
        key=bytes(config['key'],"utf-8")
        #instantiate decrypter
        fernet=Fernet(key)
        #convert to byte stream
        password=bytes(password,"utf-8")
        #decrypt password
        password=fernet.decrypt(password).decode()
        print(f"decrypted password: {password}")
    
    except Exception as ex:
        raise ex
        
    return password