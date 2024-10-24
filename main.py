#Este es el main bueno
import json
import os
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

clave = Fernet.generate_key()
clave_str = clave.decode('utf-8')
ruta = "Base de datos/clave_servidor.txt"
with open (ruta, 'w')as archivo:
    archivo.write(clave_str)







"""
password = b"notas"
print(password)
salt = os.urandom(16)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
print("token:", key)
f = Fernet()

contra_crip = f.encrypt(key)
print("key_encriptada: ", contra_crip)
contraseña = f.decrypt(contra_crip)
print("token: ",contraseña)


"""