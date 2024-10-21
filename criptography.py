
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Cripto():
    def __init__(self):
        pass

    def crear_salt(self):
        salt = os.urandom(16)
        return salt

    def crear_token(self, salt, mensaje):
        mensaje_bytes = mensaje.encode() #Transforma la parte 
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            )
        key = base64.urlsafe_b64encode(kdf.derive(mensaje_bytes))
        return key

prueba = Cripto()
s1 = prueba.crear_salt()
t1 = prueba.crear_token(s1, "hola")
t2 = prueba.crear_token(s1,"hola")
t1 =t1.hex()
t2= t2.hex()
print(t1)
print(t2)

print(t1 == t2)
    
"""password = b"notas"
print(password)
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
print(key)
f = Fernet(key)
contra_crip = f.encrypt(password)
print(contra_crip)
contraseña = f.decrypt(contra_crip)
print(contraseña)
"""