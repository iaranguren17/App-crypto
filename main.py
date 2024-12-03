from pathlib import Path
import os
from hacienda import Menus
from criptography import Cripto
from keyboardInterrupt import ki
from cerificates import Certificates
def main():
    menu = Menus()
    certificados = Certificates()
    ruta_organizaciones = "Organizaciones/Agencia_Tributaria.pem"
    directorio = os.path.dirname(ruta_organizaciones)
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    if not os.path.exists(ruta_organizaciones) or (os.path.exists(ruta_organizaciones) and os.stat(ruta_organizaciones).st_size == 0):
        certificados.create_root_certificate()
        certificados.create_intermidiates_certificates()
        certificados.create_serv_hacienda_certificate()
    
    ruta_b_d_Hacienda = Path("Organizaciones/Servidor_Hacienda/Base_de_datos.json")
    if not ruta_b_d_Hacienda.exists():
    # Crear el archivo vacío
        ruta_b_d_Hacienda.touch()
        ruta ="Base_de_datos_Hacienda_temp.json"
        with open(ruta, 'rb') as archivo:
                morosos = archivo.read()
        ruta_mensaje = "Organizaciones/Servidor_Hacienda/Base_de_datos.json"

        with open(ruta_mensaje, 'wb') as archivo:
                archivo.write(morosos)

    try:
        menu.inicio()
    except KeyboardInterrupt:
        a = ki()
        a.Interrupt()

if __name__== "__main__":
    main()