from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import NameOID
from cryptography.x509.oid import AuthorityInformationAccessOID
from cryptography import x509
from datetime import datetime, timedelta
import random
from criptography import Cripto

class certificates():
    def __init__(self):
        pass
    
    def create_root_certificate(self):
        cripto = Cripto()
        root_key = cripto.generate_private_key()

        root_name = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Ministerio de Hacienda"),
            x509.NameAttribute(NameOID.COMMON_NAME, "CA Raíz Ministerio de Hacienda"),
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
        public_key_pem = root_key.public_key().public_bytes(
                         encoding=serialization.Encoding.PEM,
                         format=serialization.PublicFormat.SubjectPublicKeyInfo
                        )
        ruta = "Organizaciones/Ministerio de Hacienda.pem"

        with open(ruta, "wb") as archivo:
            archivo.write(cert_pem)
            archivo.write(private_key_pem)
            archivo.write(public_key_pem)

a = certificates()
a.create_root_certificate()