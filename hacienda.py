import json
import os
import getpass
import re
from criptography import Cripto
from keyboardInterrupt import ki

class Menus():
    def __init__(self):
        pass
    
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
            cripto = Cripto()              #Creamos una clase Cripto
            cripto.desencriptar_json_usuarios()
            ruta_archivo = os.path.join("Base de datos", "usuarios.json")
            usuarios= self.cargar_json(ruta_archivo)
            
            nombre_usuario = str(input("\nIntroduce nombre de usuario: "))
            
            while nombre_usuario in usuarios:       #En caso de que el nombre ya esta encriptado
                print("Usuario ya registrado")
                option = int(input("Indica operación\n1:Iniciar sesión\n2:Cambiar nombre de registro \n3:Salir\n"))
                while option not in [1,2,3] :
                    option= int(input("Por favor, elige una opción correcta: \n"))
                if option == 1:
                    cripto.encriptar_json_usuarios()
                    self.login()
                elif option == 2:
                    nombre_usuario = str(input("Escribe de nuevo el nombre de usuario: "))
                else:
                    cripto.encriptar_json_usuarios()
                    return self.salir()
            
            contraseña = self.pedir_contraseña() #Creamos una contraseña
            salt_usuario = cripto.crear_salt()  #Creamos un salt por usuario
            token_usuario = cripto.crear_token(salt_usuario, contraseña)  #Y el token de la contraseña

            usuarios[nombre_usuario]= {
                "salt": salt_usuario.hex(),
                "token": token_usuario.hex()
            }
            
            self.subir_json(ruta_archivo, usuarios)
            
            cripto.encriptar_json()
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
            cripto = Cripto()
            cripto.desencriptar_json_usuarios()
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

            token = cripto.crear_token(salt_usuario, contraseña_usuario )
            token = token.hex()
            while token_usuario != token:
                intentos -= 1
                if intentos == 0:
                    print("Intentos máximos permitidos")
                    cripto.encriptar_json_usuarios()
                    return True
                print("Contraseña incorrecta. Intentos restantes: "+ str(intentos))
                contraseña_usuario = getpass.getpass("Contraseña: ")
                token = cripto.crear_token(salt_usuario, contraseña_usuario )
                token =token.hex()
            cripto.encriptar_json_usuarios()
            print("Inicio de sesión exitoso")
            return self.pantalla_morosos()
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(1)

    def pantalla_morosos(self):
        fin = False
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
                print("\nCargando página anterior...")
                fin = True
        

    def nuevo_moroso(self):
        try:
            cripto = Cripto()
            cripto.desencriptar_json_morosos()
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
            cripto.encriptar_json_morosos()
            return
        
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(2)

                    
    
    def borrar_moroso(self):
        try:
            cripto = Cripto()
            cripto.desencriptar_json_morosos()
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
            cripto.encriptar_json_morosos()
            return
        except KeyboardInterrupt:
            a = ki()
            a.Interrupt(2)
    
    def listado(self):
        try:
            cripto = Cripto()
            cripto.desencriptar_json_morosos()
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
            cripto.encriptar_json_morosos()
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



