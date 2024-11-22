from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import NameOID
from cryptography.x509.oid import AuthorityInformationAccessOID
from cryptography import x509
from datetime import datetime, timedelta
import random
from criptography import Cripto
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives.asymmetric import padding

class Certificates():
    def __init__(self):
        pass
    
    def create_root_certificate(self):
        cripto = Cripto()
        root_key = cripto.generate_private_key()

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
        cripto = Cripto()       
        
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
            intermediate_key = cripto.generate_private_key() 
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

        cripto = Cripto()       
        user_key = cripto.generate_private_key() 
        
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
                        )
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
"""

a= Certificates()
b,c,d = a.create_user_certificate("Juan","Madrid")
print(b)
print(c)
print(d)"""