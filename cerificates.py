from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import NameOID
from cryptography.x509.oid import AuthorityInformationAccessOID
from cryptography import x509
from datetime import datetime, timedelta
import random, json, os
from criptography import Cripto
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

class Certificates():
    def __init__(self):
        self.cripto = Cripto()
    
    def create_root_certificate(self):
        root_key = self.cripto.generate_private_key()

        root_name = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Ministerio_de_Hacienda"),
            x509.NameAttribute(NameOID.COMMON_NAME, "CA Raíz Ministerio_de_Hacienda"),
        ])

        #Certificado autofirmado

        root_cert = x509.CertificateBuilder()\
                    .subject_name(root_name)\
                    .issuer_name(root_name)\
                    .public_key(root_key.public_key())\
                    .serial_number(random.randint(1, 1000000))\
                    .not_valid_before(datetime.utcnow())\
                    .not_valid_after(datetime.utcnow() + timedelta(days=3650))\
                    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)\
                    .sign(private_key=root_key, algorithm=SHA256())
        
        #Convertimos el certificado, la public y private key en formato pem
        
        cert_pem = root_cert.public_bytes(encoding=serialization.Encoding.PEM)
        private_key_pem = root_key.private_bytes(
                          encoding=serialization.Encoding.PEM,
                          format=serialization.PrivateFormat.TraditionalOpenSSL,
                          encryption_algorithm=serialization.NoEncryption()  
                          )
        ruta = "Organizaciones/Ministerio_de_Hacienda.pem"

        with open(ruta, "wb") as archivo:
            archivo.write(cert_pem)
            archivo.write(private_key_pem)
            

    def create_intermidiates_certificates(self):
        ruta= "Organizaciones/Ministerio_de_Hacienda.pem"
        with open(ruta, "rb") as pem_file:
            root_key = serialization.load_pem_private_key(
                          pem_file.read(),
                          password=None  
                          )
        with open(ruta, "rb") as pem_file:
            root_certificate = load_pem_x509_certificate(pem_file.read())
        
        intermediate_org_names = ["Colegio Inspectores Madrid", "Colegio Inspectores Barcelona", "Agencia Tributaria"]
        for i in intermediate_org_names:
            intermediate_key = self.cripto.generate_private_key() 
            certificate_name = x509.Name([
                        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
                        x509.NameAttribute(NameOID.ORGANIZATION_NAME, i),
                        x509.NameAttribute(NameOID.COMMON_NAME, "CA Intermediate "+ i),
                    ])
            intermediate_cert = x509.CertificateBuilder()\
            .subject_name(certificate_name)\
            .issuer_name(root_certificate.subject)\
            .public_key(intermediate_key.public_key())\
            .serial_number(random.randint(1, 1000000))\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=1825))\
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)\
            .sign(private_key=root_key, algorithm=SHA256())

            interm_cert_pem = intermediate_cert.public_bytes(encoding=serialization.Encoding.PEM)
            private_key_pem = intermediate_key.private_bytes(
                          encoding=serialization.Encoding.PEM,
                          format=serialization.PrivateFormat.TraditionalOpenSSL,
                          encryption_algorithm=serialization.NoEncryption()  
                          )
            ruta = f"Organizaciones/{i.replace(' ', '_')}.pem"
            with open(ruta, "wb") as archivo:
                archivo.write(interm_cert_pem)
                archivo.write(private_key_pem)


    def create_user_certificate(self, name, father):
       
        user_key = self.cripto.generate_private_key()
        
        if father == "Barcelona":
            ruta= "Organizaciones/Colegio_Inspectores_Barcelona.pem"
        else:    
            ruta= "Organizaciones/Colegio_Inspectores_Madrid.pem"
        with open(ruta, "rb") as pem_file:
                inter_key = serialization.load_pem_private_key(
                            pem_file.read(),
                            password=None  
                            )
        with open(ruta, "rb") as pem_file:
                inter_certificate = load_pem_x509_certificate(pem_file.read())
            
        certificate_name = x509.Name([
                        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
                        x509.NameAttribute(NameOID.ORGANIZATION_NAME, name),
                        x509.NameAttribute(NameOID.COMMON_NAME, "CA User "+ name),
                    ])
        user_cert = x509.CertificateBuilder()\
            .subject_name(certificate_name)\
            .issuer_name(inter_certificate.subject)\
            .public_key(user_key.public_key())\
            .serial_number(random.randint(1, 1000000))\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=1825))\
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)\
            .sign(private_key= inter_key, algorithm=SHA256())
        
        user_public_key = user_cert.public_key()
        user_cert_pem = user_cert.public_bytes(encoding=serialization.Encoding.PEM).decode("utf-8")
        user_key_pem = user_key.private_bytes(
                          encoding=serialization.Encoding.PEM,
                          format=serialization.PrivateFormat.TraditionalOpenSSL,
                          encryption_algorithm=serialization.NoEncryption()  
                          ).decode("utf-8")
        public_key_pem = user_public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,  # Formato PEM
                        format=serialization.PublicFormat.SubjectPublicKeyInfo  # Estandarizado para certificados
                        ).decode("utf-8")
        return user_cert_pem, user_key_pem, public_key_pem

    def verify_certificate(self, child_cert, parent_cert):
        try:
            # Extraer la clave pública del certificado padre
            parent_public_key = parent_cert.public_key()
            
            # Verificar la firma del certificado hijo
            parent_public_key.verify(
                signature=child_cert.signature,
                data=child_cert.tbs_certificate_bytes,  # Contenido a firmar
                padding=padding.PKCS1v15(),  # Padding RSA estándar
                algorithm=SHA256()  # Algoritmo de hash
            )
            print("La firma del certificado hijo es válida.")
            return True
        except Exception as e:
            print(f"Error: La firma no es válida. Detalles: {e}")
            return False


    def create_serv_hacienda_certificate(self):
        user_key = self.cripto.generate_private_key()
        ruta= "Organizaciones/Agencia_Tributaria.pem"
        with open(ruta, "rb") as pem_file:
                inter_key = serialization.load_pem_private_key(
                            pem_file.read(),
                            password=None  
                            )
        with open(ruta, "rb") as pem_file:
                inter_certificate = load_pem_x509_certificate(pem_file.read())        

        certificate_name = x509.Name([
                        x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
                        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Servidor Hacienda"),
                        x509.NameAttribute(NameOID.COMMON_NAME, "CA User Servidor Hacienda"),
                    ])
        user_cert = x509.CertificateBuilder()\
            .subject_name(certificate_name)\
            .issuer_name(inter_certificate.subject)\
            .public_key(user_key.public_key())\
            .serial_number(random.randint(1, 1000000))\
            .not_valid_before(datetime.utcnow())\
            .not_valid_after(datetime.utcnow() + timedelta(days=1825))\
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)\
            .sign(private_key= inter_key, algorithm=SHA256())

        cert_pem = user_cert.public_bytes(encoding=serialization.Encoding.PEM)
        private_key_pem = user_key.private_bytes(
                          encoding=serialization.Encoding.PEM,
                          format=serialization.PrivateFormat.TraditionalOpenSSL,
                          encryption_algorithm=serialization.NoEncryption()  
                          )
        ruta = "Organizaciones/Servidor_Hacienda.pem"

        with open(ruta, "wb") as archivo:
            archivo.write(cert_pem)
            archivo.write(private_key_pem)
    
    def load_certificate_from_file(self, file_path):
         with open(file_path, "rb") as file:
              return x509.load_pem_x509_certificate(file.read(), default_backend())
    
    def load_public_key_from_file(self, file_path):
        with open(file_path, "rb") as file:
            return serialization.load_pem_public_key(file.read(), backend=default_backend())
        
    def load_certificate_from_json(self, json_path, inspector_name):
        try:
            self.cripto.desencriptar_json_usuarios()
            with open(json_path, "r") as file:
                data = json.load(file)

            if inspector_name not in data:
                raise ValueError(f"El inspector '{inspector_name}' no se encuentra en el archivo JSON.")

            inspector_cert_pem = data[inspector_name]["Certificado"]
            temp_cert_path = f"temp_{inspector_name.replace(' ', '_')}.pem"
            with open(temp_cert_path, "w") as temp_file:
                temp_file.write(inspector_cert_pem)
            
            self.cripto.encriptar_json_usuarios()
            return temp_cert_path
        except Exception as e:
            print(f"Error al cargar el certificado del inspector desde JSON: {e}")
            self.cripto.encriptar_json_usuarios()
            return None
           
    def verify_certificate_chain(self, cert_path, chain_paths):
        try:
            child_cert = self.load_certificate_from_file(cert_path)
            for chain_path in chain_paths:
                parent_cert = self.load_certificate_from_file(chain_path)
                parent_public_key = parent_cert.public_key()
                parent_public_key.verify(
                    signature = child_cert.signature,
                    data = child_cert.tbs_certificate_bytes,
                    padding = padding.PKCS1v15(),
                    algorithm = SHA256()
                )
                print(f"Certificado {child_cert.subject.rfc4514_string()} validado con {parent_cert.subject.rfc4514_string()}")
                child_cert = parent_cert
            print("La cadena de confianza es válida")
            return True
           
        except Exception as e:
             print(f"Error al validar la clave pública: {e}")
             return False
        
    def verify_inspector_certificates(self, json_path, inspector_name, chain_paths):
        cert_path = self.load_certificate_from_json(json_path, inspector_name)
        if not cert_path:
            return False
        
        is_valid = self.verify_certificate_chain(cert_path, chain_paths)
        
        if os.path.exists(cert_path):
            os.remove(cert_path)
        
        return is_valid
        

             
certificates = Certificates()
cert_path = "Organizaciones/Servidor_Hacienda.pem"
chain_paths = [
    "Organizaciones/Agencia_Tributaria.pem",
    "Organizaciones/Ministerio_de_Hacienda.pem"
]

if certificates.verify_certificate_chain(cert_path, chain_paths):
    print("La cadena de certificados del servidor Hacienda es válida.")
else:
    print("La cadena de certificados del servidor Hacienda no es válida.")   
    

