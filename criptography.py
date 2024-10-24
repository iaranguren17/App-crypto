
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json 

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

    def leer_clave_servidor(self):
        ruta = "Base de datos/clave_servidor.txt"
        with open (ruta, 'r') as archivo_clave:
            clave = archivo_clave.read()
        
        clave = clave.encode('utf-8')
        return clave

    """
    def desencriptar_json(self):
        ruta= "Base de datos/usuarios.json"
        if os.path.exists(ruta):
            with open(ruta, 'rb') as archivo: #'rb' read in bits
                datos_encriptados = archivo.read()
        
        if len(datos_encriptados) == 0:
            return
       
        clave = self.leer_clave_servidor()
        fernet = Fernet(clave)
        datos_desencriptados = fernet.decrypt(datos_encriptados)
        json_desencriptado = json.loads(datos_desencriptados.decode('utf-8'))
        return self.sobrescribir_json(ruta, json_desencriptado)
"""
    def sobrescribir_json(self,ruta, contenido):
        with open(ruta, 'w') as archivo:
            json.dump(contenido, archivo, indent=4)
        return 

    def encriptar_json(self):
        ruta= "Base de datos/usuarios.json"
        if os.path.exists(ruta):
            with open(ruta, 'rb') as archivo: #'rb' read in bits
                datos_desencriptados = archivo.read()
        clave = self.leer_clave_servidor()
        fernet = Fernet(clave)
        datos_encriptados = fernet.encrypt(datos_desencriptados)
        return self.sobrescribir_json(ruta, datos_encriptados)





prueba = Cripto()
prueba.encriptar_json
"""
s1 = prueba.crear_salt()
t1 = prueba.crear_token(s1, "hola")
t2 = prueba.crear_token(s1,"hola")
t1 =t1.hex()
t2= t2.hex()
print(t1)
print(t2)

print(t1 == t2)

    
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
print(key)
f = Fernet(key)
contra_crip = f.encrypt(password)
print(contra_crip)
contraseña = f.decrypt(contra_crip)
print(contraseña)
"""