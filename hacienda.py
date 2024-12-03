import json
import os
import getpass
import re
from criptography import Cripto
from keyboardInterrupt import ki
from cerificates import Certificates
class Menus():
    def __init__(self):
        self.cripto = Cripto()
        self.certificates = Certificates()
    def salir(self):
        print("\nMuchas gracias, hasta la próxima\nFIN DE PROGRAMA")
        return True

    def inicio(self):
        welcome_messg = """ __    __   ______    ______   ______  ________  __    __  _______    ______        
/  |  /  | /      \  /      \ /      |/        |/  \  /  |/       \  /      \       
$$ |  $$ |/$$$$$$  |/$$$$$$  |$$$$$$/ $$$$$$$$/ $$  \ $$ |$$$$$$$  |/$$$$$$  |      
$$ |__$$ |$$ |__$$ |$$ |  $$/   $$ |  $$ |__    $$$  \$$ |$$ |  $$ |$$ |__$$ |      
$$    $$ |$$    $$ |$$ |        $$ |  $$    |   $$$$  $$ |$$ |  $$ |$$    $$ |      
$$$$$$$$ |$$$$$$$$ |$$ |   __   $$ |  $$$$$/    $$ $$ $$ |$$ |  $$ |$$$$$$$$ |      
$$ |  $$ |$$ |  $$ |$$ \__/  | _$$ |_ $$ |_____ $$ |$$$$ |$$ |__$$ |$$ |  $$ |      
$$ |  $$ |$$ |  $$ |$$    $$/ / $$   |$$       |$$ | $$$ |$$    $$/ $$ |  $$ |      
$$/   $$/ $$/   $$/  $$$$$$/  $$$$$$/ $$$$$$$$/ $$/   $$/ $$$$$$$/  $$/   $$/            
--------------------------------------------------------------------------------                                                       
"""


        print("\n", welcome_messg)
        fin = False
        while not fin:
            print("--------------------------------------------------------------------------------")
            print("INICIO")
            print("--------------------------------------------------------------------------------")

            accion = int(input("Selecciona una opción: \n1-Registrarse \n2-Iniciar sesión \n3-Salir\nIntroduce el número de la acción: "))
            while accion not in [1,2,3]:
                accion = int(input("Por favor escoge una opción correcta: "))
            if accion == 1:
                fin = self.registrar_usuario()
            elif accion == 2:
                fin = self.login()
            else:
                fin = self.salir()
        
   
    def registrar_usuario(self):
        print("--------------------------------------------------------------------------------")
        print("REGISTRARSE")
        print("--------------------------------------------------------------------------------")
        try:
                         #Creamos una clase Cripto
            self.cripto.desencriptar_json_usuarios()
            ruta_archivo = os.path.join("Base de datos", "usuarios.json")
            usuarios= self.cargar_json(ruta_archivo)
            
            nombre_usuario = str(input("\nIntroduce nombre de usuario: "))
            
            while nombre_usuario in usuarios:       #En caso de que el nombre ya esta encriptado
                print("Usuario ya registrado")
                option = int(input("Indica operación\n1:Iniciar sesión\n2:Cambiar nombre de registro \n3:Salir\n"))
                while option not in [1,2,3] :
                    option= int(input("Por favor, elige una opción correcta: \n"))
                if option == 1:
                    self.cripto.encriptar_json_usuarios()
                    self.login()
                elif option == 2:
                    nombre_usuario = str(input("Escribe de nuevo el nombre de usuario: "))
                else:
                    self.cripto.encriptar_json_usuarios()
                    return self.salir()
            
            contraseña = self.pedir_contraseña() #Creamos una contraseña
            salt_usuario = self.cripto.crear_salt()  #Creamos un salt por usuario
            token_usuario = self.cripto.crear_token(salt_usuario, contraseña)  #Y el token de la contraseña
            print("¿Perteneces a qué colegio de inspectores) \n1:Barcelona \n2:Madrid")
            
            colegio = int(input("Elige opción: "))
            while (colegio != 1 and colegio != 2):
                print("Opción no válida. Por favor escoja na opción correcta")
                print("¿Perteneces a qué colegio de inspectores) \n1:Barcelona \n2:Madrid")
                colegio = int(input("Elige opción: "))
            
            if colegio == 1:
                ciudad = "Barcelona"
                
            else:
                ciudad = "Madrid"
            
            user_cert, user_key, user_public_key = self.certificates.create_user_certificate(nombre_usuario, ciudad)
            
            usuarios[nombre_usuario]= {
                "salt": salt_usuario.hex(),
                "token": token_usuario.hex(),
                "ciudad": ciudad,
                "Certificado": user_cert,
                "Public_key": user_public_key,
                "Private_key": user_key
            }
            
            self.subir_json(ruta_archivo, usuarios)
            
            self.cripto.encriptar_json_usuarios()
            print("Usuario registrado correctamente")
            print("--------------------------------------------------------------------------------")
            
            return False
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(1)


    def pedir_contraseña(self):
        try: 
            contraseña_segura = False
            while not contraseña_segura:
                contraseña = str(getpass.getpass("Introduce contraseña: "))
                contraseña_segura = self._verificar_contraseña(contraseña)
            print("Contraseña segura")
            return contraseña 
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(1)
            
    
    def _verificar_contraseña(self, contraseña):
        if len(contraseña) < 12:
            print("Contraseña demasiado pequeña")
            print("La contraseña debe tener mínimo 12 caracteres, una mayúscula, una minúscula y un número")
            return False
        
        mayus = False
        minus = False
        numero = False
        
        for i in contraseña:
            if i.isupper():
                mayus = True
            elif i.islower():
                minus = True
            elif i.isdigit():
                numero = True

        if not mayus:
            print("Falta una letra mayúscula")
        if not minus:
            print("Falta una letra minúscula")
        if not numero:
            print("Falta un número")
        if numero and minus and mayus:
            repetir_contraseña = getpass.getpass("Confirmar contraseña: ")
            if contraseña != repetir_contraseña:
                print("Contraseñas incorrectas")
                return False
            else:
                return True

        return False


    def login(self):
        print("--------------------------------------------------------------------------------")
        print("INICIO DE SESIÓN")
        print("--------------------------------------------------------------------------------")
        try:
            self.cripto.desencriptar_json_usuarios()
            ruta_archivo = os.path.join("Base de datos", "usuarios.json")
            usuarios = self.cargar_json(ruta_archivo)

            
            nombre_usuario = input("\nUsuario: ")
            while nombre_usuario not in usuarios:
                opcion=int(input("Usuario incorrecto.\n1:Volver a intentar\n2:Salir\n"))
                while opcion not in [1,2]:
                    opcion = int(input("Por favor, elija una opción válida: \n" ))
                if opcion == 1:
                    nombre_usuario = input("\nUsuario: ")
                else:
                    return False
            intentos = 4
            contraseña_usuario = getpass.getpass("Contraseña: ")
            
            token_usuario = usuarios[nombre_usuario]["token"]
            salt_usuario = usuarios[nombre_usuario]["salt"]
            salt_usuario = bytes.fromhex(salt_usuario)
            ciudad_usuario = usuarios[nombre_usuario]["ciudad"]

            token = self.cripto.crear_token(salt_usuario, contraseña_usuario )
            token = token.hex()
            while token_usuario != token:
                intentos -= 1
                if intentos == 0:
                    print("Intentos máximos permitidos")
                    self.cripto.encriptar_json_usuarios()
                    return True
                print("Contraseña incorrecta. Intentos restantes: "+ str(intentos))
                contraseña_usuario = getpass.getpass("Contraseña: ")
                token = self.cripto.crear_token(salt_usuario, contraseña_usuario )
                token =token.hex()
            self.cripto.encriptar_json_usuarios()
            print("Verificando certificaciones...")

            if ciudad_usuario == "Madrid":
                chain_path = ["Organizaciones/Colegio_Inspectores_Madrid.pem","Organizaciones/Ministerio_de_Hacienda.pem"]
            else:
                chain_path = ["Organizaciones/Colegio_Inspectores_Barcelona.pem","Organizaciones/Ministerio_de_Hacienda.pem"]

            chain_serv = ["Organizaciones/Agencia_Tributaria.pem","Organizaciones/Ministerio_de_Hacienda.pem"]
            cert_path = "Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem"

            self.certificates.verify_inspector_certificates(ruta_archivo, nombre_usuario, chain_path)
            self.certificates.verify_certificate_chain(cert_path, chain_serv)
            print("Certificados verificados correctamente")
            
            print("Inicio de sesión exitoso")
            return self.pantalla_morosos(nombre_usuario)
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(1)

    def pantalla_morosos(self, inspector):
        try:    
            
            #En pantalla del Inspector
            
            print("Recibiendo datos de Hacienda...")
            fin = False
            
            a = input("Enter1")
            #Actuamos como Servidor Hacienda
            #Primero desencriptamos con nuestra privada la base de datos, si esta no esta vacía
            
            self.cripto.desencriptar_json_inicial_hacienda()
            a = input("Enter2")        
            #Sacamos la firma y comprobamos que es correcta
            with open("Organizaciones/Servidor_Hacienda/Base_de_datos.json", "r") as archivo:
                mensaje_firma = json.load(archivo)
            firma = mensaje_firma["firma"]
            mensaje = mensaje_firma["mensaje"]
            mensaje_serializado = json.dumps(mensaje).encode('utf-8')
            firma_bytes = bytes.fromhex(firma)
            public_key = self.cripto.extraer_public_key("Organizaciones/Servidor_Hacienda/Servidor_Hacienda.pem")
            if not  self.cripto.verificar_firma(public_key, firma_bytes, mensaje_serializado):
                print("Problema de seguridad de la base de datos.\nPor favor, espere a que se resuelva")
                return 
            a = input("Enter3")   
            #Una vez  ferificado su firma, solo es necesario que mande los mensajes
            with open("Organizaciones/Servidor_Hacienda/Base_de_datos.json", "w") as archivo:
                archivo.write(json.dumps(mensaje))
            a = input("Enter4")            
            #Ahora hay que crear una clave de Sesión, que sera Chacha20
            clave_sesión = self.cripto.generar_clave_chacha20()
            a = input("Enter5")
            with open("Organizaciones/Servidor_Hacienda/clave_sesión.txt", 'wb') as archivo_clave:  # Guardamos la clave en binario
                archivo_clave.write(clave_sesión)
            a = input("Enter6")
            #La ciframos y la dejamos lista para enviar
            self.cripto.cifrar_clave_sesión(inspector, clave_sesión)
            a = input("Enter7")
            #Ahora toca hacer lo mismo con el mensaje
            self.cripto.cifrar_mensaje(clave_sesión)

            #Una vez enviado todo toca ser El Inspector
            print("Comprobando Información")
            #Primero tenemos que extraer la clave de sesión y comprobar la firma
            a = input("Enter8")
            verify = self.cripto.desencriptar_clave_sesion(inspector)
            if not verify:
                return
            a = input("Enter9")
            #Una vez sacada la clave, desencriptamos el mensaje
            verify = self.cripto.desencriptar_mensaje()
            if not verify:
                return
            #Actualizamos la base de datos del inspector    
            while not fin:
                print("--------------------------------------------------------------------------------")
                print("LISTA DE MOROSOS")
                print("--------------------------------------------------------------------------------")

                accion = int(input("Selecciona una opción: \n1-Añadir moroso \n2-Borrar moroso \n3-Ver lista \n4-Salir\nIntroduce el número de la acción: "))
                while accion not in [1,2,3,4]:
                    accion = int(input("Por favor escoge una opción correcta: "))
                if accion == 1:
                    fin = self.nuevo_moroso()
                elif accion == 2:
                    fin = self.borrar_moroso()
                elif accion == 3:
                    fin = self.listado()
                else: 
                    a = input("Enter10")

                #Mandamos a Hacienda la lista actualizada y borramos la base de datos temporal, y la clave de sesión nuestra parte
                    self.cripto.enviar_a_hacienda()
                #Una vez madado el mensaje, volvemos a actuar como Hacienda
                    a = input("Enter11")
                #Cogemos el mensaje y lo actualizamos en la base de datos
                    self.cripto.actualizar_base_de_datos()    
                    a = input("Enter12")
                #Cifrado final del Servidor de Hacienda
                    self.cripto.encriptar_json_final_hacienda()
                    a = input("Enter13")
                    print("Proceso Terminado con éxito")
                    print("\nCargando página anterior...")
                    fin = True
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(1)
        

    def nuevo_moroso(self):
        try:
            self.cripto.desencriptar_json_morosos()
            ruta_archivo = os.path.join("Base de datos", "morosos.json")
            morosos = self.cargar_json(ruta_archivo)

            numero_ss = str(input("\nIntroduce el numero de la SS del moroso: "))
            while not re.fullmatch(r"^\d{8}$", numero_ss):
                numero_ss = str(input("\nFormato no válido, tiene que tener 8 dígitos: "))
                
            if numero_ss in morosos:       #En caso de que el nombre ya esta encriptado
                print("Moroso ya registrado")
                return
            
            deuda = str(input("Introduzca la deuda del moroso: "))
            tiempo_deuda = str(input("Introduzca cuanto tiempo lleva con la deuda: "))

            morosos[numero_ss]= {
                "deuda": deuda,
                "endeudado": tiempo_deuda
            }
            
            self.subir_json(ruta_archivo, morosos)

            print("Moroso añadido correctamente")
            print("--------------------------------------------------------------------------------\n")
            self.cripto.encriptar_json_morosos()
            return
        
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(2)

                    
    
    def borrar_moroso(self):
        try:
            self.cripto.desencriptar_json_morosos()
            ruta_archivo = os.path.join("Base de datos", "morosos.json")
            morosos = self.cargar_json(ruta_archivo)

            numero_ss = str(input("\nIntroduce el numero de la SS del moroso: "))
            while not re.fullmatch(r"^\d{8}$", numero_ss):
                numero_ss = str(input("\nFormato no válido, tiene que tener 8 dígitos: "))

            if numero_ss not in morosos:
                print("Moroso no registrado")
                return
            
            del morosos[numero_ss]
            self.subir_json(ruta_archivo, morosos)

            print("Moroso borrado correctamente")
            print("--------------------------------------------------------------------------------")
            self.cripto.encriptar_json_morosos()
            return
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(2)
    
    def listado(self):
        try:
            self.cripto.desencriptar_json_morosos()
            ruta_archivo = os.path.join("Base de datos", "morosos.json")
            morosos = self.cargar_json(ruta_archivo)

            if not morosos:
                print("No hay morosos registrados.")
                return

            print("--------------------------------------------------------------------------------")
            print("LISTADO DE MOROSOS")
            print("--------------------------------------------------------------------------------")
            for numero_ss, info in morosos.items():
                deuda = info.get("deuda", "N/A")
                tiempo_deuda = info.get("endeudado", "N/A")
                print(f"Número SS: {numero_ss}")
                print(f"  - Deuda: {deuda} €")
                print(f"  - Tiempo con deuda: {tiempo_deuda}")
                print("--------------------------------------------------------------------------------")
            self.cripto.encriptar_json_morosos()
            return
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(2)                


    def cargar_json(self, ruta_archivo):
        directorio = os.path.dirname(ruta_archivo)
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"El directorio {directorio} no existía y ha sido creado.")

        if not os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'w') as archivo:
                json.dump({}, archivo)  # Escribir un JSON vacío en el archivo
            print(f"El archivo {ruta_archivo} no existía y ha sido creado.")

        with open(ruta_archivo, 'r') as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                print(f"Advertencia: El archivo {ruta_archivo} está modificado o tiene un formato JSON no válido.")
                exit(1)
                return {}
            except Exception as e:
                raise Exception(f"Ocurrió un error al cargar el archivo {ruta_archivo}: {e}")


        
    def subir_json(self, ruta_archivo, list):
        with open(ruta_archivo, 'w') as archivo:
            json.dump(list, archivo, indent=4)


