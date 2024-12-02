
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
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization


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
                print("Clave de sesión creada con éxito")
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
        if not os.path.exists(ruta):
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
    
    #genera un hash del mensaje
    def generate_hash(self, message):
        hash = hashes.Hash(hashes.SHA256())
        if isinstance(message, bytes):
            message_data = message
        else:
            message_data = message.encode('utf-8')
        hash.update(message_data)
        result = hash.finalize()
        return result
    
    #Extrae la public key en formato objeto      
    def extraer_public_key(self, ruta:str):
        with open(ruta, "rb") as pem_file:
            certificate = load_pem_x509_certificate(pem_file.read())

        return certificate.public_key()
    
    #Extrae la private key en formato objeto 
    def extraer_private_key(self, ruta:str):
        with open(ruta, "rb") as pem_file:
            private_key = serialization.load_pem_private_key(
                        pem_file.read(),
                        password=None  
                        )
        return private_key

    def encript_with_rsa(self,key,message):
        if isinstance(message, bytes):
            bit_message = message
        else:
            bit_message = message.encode('utf-8')
        
        ciphertext = key.encrypt(
                    bit_message,
                    padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                                )               
                    )
        return ciphertext
    
    def decrypt_with_rsa(self,private_key,encript_message):
        plaintext = private_key.decrypt(
                    encript_message,
                    padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None))
        return plaintext
    
    def firma(self, message, private_key):
        if isinstance(message, bytes):
            bytes_message = message
        else:
            bytes_message = message.encode('utf-8')
        signature = private_key.sign(
                    bytes_message,
                    padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                    )
        return signature
    
    def verificar_firma(self, public_key, signature, message):
        try: 
            public_key.verify(
                signature,
                message,
                padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            return True
        except Exception :
            return False
    
    def encriptar_json_final_hacienda(self):
        ruta ="Base de datos/morosos.json"
        with open(ruta, "r") as archivo:
            lista_morosos = json.load(archivo)
        #Firma del mensaje
        lista_morosos_bytes = json.dumps(lista_morosos).encode('utf-8')
        private_key = self.extraer_private_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        firma =  self.firma(lista_morosos_bytes, private_key)
        #Añadimos la firma al mensaje
        mensaje_firmado ={
            "mensaje" : lista_morosos,
            "firma" : firma.hex()
                    }
        
        #Transformamos el mensaje firmado a bytes
        mensaje_firmado_serializado = json.dumps(mensaje_firmado).encode('utf-8')
        #Vamos encriptando en fragmentos de 190B con RSA
        public_key = self.extraer_public_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        encripted_list = []
        inicio = 0
        fragment_size = 190
        while inicio < len(mensaje_firmado_serializado):
            fin = min(inicio + fragment_size, len(mensaje_firmado_serializado))
            encripted_part = self.encript_with_rsa(public_key, mensaje_firmado_serializado[inicio:fin])
            encripted_list.append(encripted_part)
            inicio = fin
        #Guardamos la base de datos
        with open(ruta, 'wb') as archivo:
            for fragment in encripted_list:
                archivo.write(fragment)  
            archivo.close()

        return 

    def desencriptar_json_inicial_hacienda(self):
        ruta = "Base de datos/morosos.json"
        with open(ruta, 'rb') as archivo:
            datos_encriptados = archivo.read()
        
        private_key = self.extraer_private_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        decripted_list = []
        inicio = 0
        fragment_size = 256
        for i in range(0,len(datos_encriptados), fragment_size):
            fragment = datos_encriptados[i: i+fragment_size]
            decripted_fragment = self.decrypt_with_rsa(private_key,fragment)
            decripted_list.append(decripted_fragment)

        decripted_message = b"".join(decripted_list)

        with open(ruta, 'w') as archivo:
            archivo.write(decripted_message.decode('utf-8'))
            
        return
    
    def cifrar_clave_sesión(self, inspector, clave_sesion):
        #Obtenemos clave pública del inspector
        self.desencriptar_json_usuarios()
        ruta_archivo = os.path.join("Base de datos", "usuarios.json")
        with open(ruta_archivo, 'r') as archivo:
            usuarios = json.load(archivo)
        public_key_pem = usuarios[inspector]["Public_key"]
        self.encriptar_json_usuarios()
        public_key_bytes = public_key_pem.encode('utf-8')
        public_key = serialization.load_pem_public_key(public_key_bytes)
        hash_clave = self.generate_hash(clave_sesion)
        private_key_hacienda = self.extraer_private_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        firma_hash = self.firma(hash_clave, private_key_hacienda)
        
        ruta_mensaje = "Mensajes/clave.json"
        directorio = os.path.dirname(ruta_mensaje)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        
        clave_firma ={
                "clave" : base64.b64encode(clave_sesion).decode('utf-8'),
                "firma_hash" : base64.b64encode(firma_hash).decode('utf-8')
        }
        
        
        clave_firma_bytes = json.dumps(clave_firma).encode('utf-8')

        encripted_list = []
        inicio = 0
        fragment_size = 190
        while inicio < len(clave_firma_bytes):
            fin = min(inicio + fragment_size, len(clave_firma_bytes))
            encripted_part = self.encript_with_rsa(public_key, clave_firma_bytes[inicio:fin])
            encripted_list.append(encripted_part)
            inicio = fin
        #Guardamos la base de datos
        
        with open(ruta_mensaje, 'wb') as archivo:
            for fragment in encripted_list:
                archivo.write(fragment)  
            archivo.close()

        return 
    
    def cifrar_mensaje(self,clave_sesion):
        ruta = "Base de datos/morosos.json"
        with open(ruta, 'r') as archivo:
            mensaje = json.load(archivo)
        mensaje_bytes = json.dumps(mensaje).encode('utf-8')
        hash = self.generate_hash(mensaje_bytes)
        
        private_key_hacienda = self.extraer_private_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        firma_hash = self.firma(hash, private_key_hacienda)
        ruta_mensaje = "Mensajes/mensaje.json"
        mensaje_firma ={
                "mensaje" : base64.b64encode(mensaje_bytes).decode('utf-8'),
                "firma_hash" : base64.b64encode(firma_hash).decode('utf-8')
        } 
        mensaje_firma_bytes = json.dumps(mensaje_firma).encode('utf-8')
        chacha = ChaCha20Poly1305(clave_sesion)
        nonce = os.urandom(12)
        datos_encriptados = chacha.encrypt(nonce, mensaje_firma_bytes, None)

        result = nonce + datos_encriptados
        with open(ruta_mensaje, "wb") as f:  # Modo binario
            f.write(result)
        return
    
    def desencriptar_clave_sesion(self,inspector):
        #Extraemos la private_key del usuario
        self.desencriptar_json_usuarios()
        ruta_archivo = os.path.join("Base de datos", "usuarios.json")
        with open(ruta_archivo, 'r') as archivo:
            usuarios = json.load(archivo)
        private_key_pem = usuarios[inspector]["Private_key"]
        self.encriptar_json_usuarios()
        private_key_bytes = private_key_pem.encode('utf-8')
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None
            )
        
        ruta = "Mensajes/clave.json"
        
        #Desciframos el mensaje
        with open(ruta, 'rb') as archivo:
            datos_encriptados = archivo.read()
        decripted_list = []
        inicio = 0
        fragment_size = 256
        for i in range(0,len(datos_encriptados), fragment_size):
            fragment = datos_encriptados[i: i+fragment_size]
            decripted_fragment = self.decrypt_with_rsa(private_key,fragment)
            decripted_list.append(decripted_fragment)

        decripted_message = b"".join(decripted_list)

        with open(ruta, 'w') as archivo:
            archivo.write(decripted_message.decode('utf-8'))

        #Comprobamos la firma haciendo un hash de la clave 
        with open(ruta, 'r') as archivo:
            usuarios = json.load(archivo)
        clave = usuarios["clave"]
        clave_bytes = base64.b64decode(clave)
        firma = usuarios["firma_hash"]
        firma_bytes = base64.b64decode(firma)
        hash_clave = self.generate_hash(clave_bytes)
        public_key_hacienda = self.extraer_public_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        if os.path.exists(ruta):
            os.remove(ruta)
        if not self.verificar_firma(public_key_hacienda, firma_bytes, hash_clave):
            print("Problema de Seguridad. Emisor desconocido")
            return False
        ruta_clave = "Base de datos/clave_chacha.txt"
        directorio = os.path.dirname(ruta_clave)
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        if not os.path.exists(ruta_clave):
            with open(ruta_clave, 'wb') as archivo_clave:  # Guardamos la clave en binario
                archivo_clave.write(clave_bytes)
                print("Clave de sesión almacenada con éxito")
    
        return True    

    def desencriptar_mensaje(self):
        ruta = "Mensajes/mensaje.json"
        clave_sesion = self.leer_clave_chacha()
        chacha = ChaCha20Poly1305(clave_sesion)
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
            print("Error al desencriptar :", e)
            return None
        
        with open(ruta, 'r') as archivo:
            mensaje_firma = json.load(archivo)
        mensaje_cod = mensaje_firma["mensaje"]
        mensaje_bytes = base64.b64decode(mensaje_cod)
        mensaje = mensaje_bytes.decode('utf-8')
        firma_cod = mensaje_firma["firma_hash"]
        firma = base64.b64decode(firma_cod)
        hash_mensaje = self.generate_hash(mensaje_bytes)
        #Comprobamos firma
        public_key_hacienda = self.extraer_public_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
        if not self.verificar_firma(public_key_hacienda, firma, hash_mensaje):
            print("Problema de Seguridad. Emisor desconocido")
            return  False
        #Guardamos en una base de datos temporal
        if os.path.exists(ruta):
            os.remove(ruta)
        ruta_morosos = "Base de datos/morosos.json"
        directorio = os.path.dirname(ruta_morosos)
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        if not os.path.exists(ruta_morosos):
            with open(ruta_morosos, 'w') as archivo_clave:  # Guardamos la clave en binario
                archivo_clave.write(mensaje)
                print("Base de datos almacenado con éxito")
        self.encriptar_json_morosos()
        return  True 

    def enviar_a_hacienda(self):
        ruta = "Base de datos/morosos.json"
        with open(ruta, 'rb') as archivo:
            morosos = archivo.read()
        ruta_mensaje = "Mensajes/mensaje.json"
        with open(ruta_mensaje, 'wb') as archivo:
            archivo.write(morosos)
        if os.path.exists(ruta):
            os.remove(ruta)
        if os.path.exists("Base de datos/clave_chacha.txt"):
            os.remove(ruta)
        return
    
    def actualizar_base_de_datos(self):
        #Desencriptamos el mensaje
        


a= Cripto()
a.enviar_a_hacienda()



