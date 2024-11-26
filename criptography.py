
import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import rsa
import json 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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
    
    def generar_clave_fernet(self):
        return Fernet.generate_key()
    
    
    def leer_clave_servidor(self):
        ruta = "Base de datos/clave_servidor.txt"
        directorio = os.path.dirname(ruta)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"El directorio {directorio} no existía y ha sido creado.")
        
        if not os.path.exists(ruta):
            clave = self.generar_clave_fernet()
            with open(ruta, 'wb') as archivo_clave:  # Guardamos la clave en binario
                archivo_clave.write(clave)
            print(f"El archivo {ruta} no existía y ha sido creado con una nueva clave.")
            return clave
        else:
            with open(ruta, 'rb') as archivo_clave:
                return archivo_clave.read()
        
    
    def generar_clave_chacha20(self):
        return os.urandom(32)
    
    def leer_clave_chacha(self):
        ruta = "Base de datos/clave_chacha.txt"
        directorio = os.path.dirname(ruta)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"El directorio {directorio} no existía y ha sido creado.")
        
        if not os.path.exists(ruta):
            clave = self.generar_clave_chacha20()
            with open(ruta, 'wb') as archivo_clave:  # Guardamos la clave en binario
                archivo_clave.write(clave)
            print(f"El archivo {ruta} no existía y ha sido creado con una nueva clave.")
            return clave
        else:
            with open(ruta, 'rb') as archivo_clave:
                return archivo_clave.read()

    def encriptar_json_usuarios(self):
        ruta= "Base de datos/usuarios.json"
        if os.path.exists(ruta):
            with open(ruta, 'rb') as archivo: #'rb' read in bits
                datos_desencriptados = archivo.read()
        clave = self.leer_clave_servidor()
        fernet = Fernet(clave)
        datos_encriptados = fernet.encrypt(datos_desencriptados)
        with open(ruta, 'wb') as archivo:  # Escribir en modo binario
            archivo.write(datos_encriptados)
        archivo.close()
        return
    
    def encriptar_json_morosos(self):
        ruta = "Base de datos/morosos.json"
        clave = self.leer_clave_chacha()
        chacha = ChaCha20Poly1305(clave)
        nonce = os.urandom(12)  

        if os.path.exists(ruta):
            with open(ruta, 'rb') as archivo:
                datos_desencriptados = archivo.read()

            datos_encriptados = chacha.encrypt(nonce, datos_desencriptados, None)

            with open(ruta, 'wb') as archivo:
                archivo.write(nonce + datos_encriptados)  # Guardar nonce + datos
            archivo.close()
        return 


    def desencriptar_json_usuarios(self):
        ruta = "Base de datos/usuarios.json"
        clave = self.leer_clave_servidor()
        fernet = Fernet(clave)
        directorio = os.path.dirname(ruta)
        if not os.path.exists(directorio):
            return
        try:
            with open(ruta, 'rb') as archivo:
                datos_encriptados = archivo.read()
            if datos_encriptados == {}:
                return
            # Intentar desencriptar los datos
            datos_desencriptados = fernet.decrypt(datos_encriptados)
            
            # Guardar los datos desencriptados de nuevo en el archivo
            with open(ruta, 'wb') as archivo:
                archivo.write(datos_desencriptados)
            archivo.close()
            return
        except InvalidToken:
            print("Error: La clave no es válida o los datos han sido modificados.")
        
        except Exception as e:
            print(f"Ocurrió un error al desencriptar usuarios.json: {e}")
    
    def desencriptar_json_morosos(self):
        ruta = "Base de datos/morosos.json"
        clave = self.leer_clave_chacha()
        chacha = ChaCha20Poly1305(clave)

        if os.path.exists(ruta):
            with open(ruta, 'rb') as archivo:
                datos_encriptados = archivo.read()
                if len(datos_encriptados) < 13:  # El tamaño mínimo es nonce (12) + 1 byte
                    return None

                nonce = datos_encriptados[:12]
                datos = datos_encriptados[12:]

                # Desencriptar los datos
                try:
                    datos_desencriptados = chacha.decrypt(nonce, datos, None)
                    with open(ruta, 'wb') as archivo:
                        archivo.write(datos_desencriptados)
                    archivo.close()
                except Exception as e:
                    print("Error al desencriptar morosos.json:", e)
                    return None
        return

    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        return private_key
    
    def generate_hash(self, message):
        hash = hashes.Hash(hashes.SHA256())
        message_data = message.encode('utf-8')
        hash.update(message_data)
        result = hash.finalize()
        return result
    """
    def encript_with_rsa(self,key,message):
        bit_message = message.encode('utf-8')
        ciphertext = key.encrypt(
                    message,
                    padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                                )               
                    )
        return ciphertext
"""