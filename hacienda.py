import json
import os
import getpass
from criptography import Encriptar

class Menus():
    def __init__(self):
        pass
    
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
        
        accion = int(input("Selecciona una opción: \n1-Registrarse \n2-Iniciar sesión \n3-Salir\nIntroduce el número de la acción: "))
        
        if accion == 1:
            self.registrar_usuario()
        elif accion == 2:
            self.login()
        elif accion == 3:
            print("\nMuchas gracias, hasta la próxima\nFIN DE PROGRAMA") 
            return
    def registrar_usuario(self):
        print("--------------------------------------------------------------------------------")
        print("REGISTRARSE")
        print("--------------------------------------------------------------------------------")

        ruta_archivo = os.path.join("Base de datos", "usuarios.json")
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                try: 
                    usuarios = json.load(archivo)   #Carga el JSON
                except json.JSONDecodeError:
                    usuarios ={}    # Si el archivo JSON esta vacío creo el diccionario

        
        nombre_usuario = str(input("\nIntroduce nombre de usuario: "))
        
        while nombre_usuario in usuarios:       #En caso de que el nombre ya esta encriptado
            print("Usuario ya registrado")
            option = input("Indica operación\n 1:Iniciar sesión\n2: Cambiar nombre de registro \n 3:Salir")
            while option not in [1,2,3] :
                option= input("Por favor, elige una opción correcta: \n")
            if option == 1:
                self.login()
            elif option == 2:
                nombre_usuario = str(input("Escribe de nuevo el nombre de usuario"))
            else:
                print("\nMuchas gracias, hasta la próxima\nFIN DE PROGRAMA")
                return
        
        contraseña = self.pedir_contraseña() #Creamos una contraseña
        encriptar = Encriptar()              #Creamos una clase Encriptar
        salt_usuario = encriptar.crear_salt()  #Creamos un salt por usuario
        token_usuario = encriptar.crear_token(salt_usuario, contraseña)  #Y el token de la contraseña
        
        usuarios[nombre_usuario]= {
            "salt": salt_usuario.hex(),
            "token": token_usuario.hex()
        }

        with open(ruta_archivo, 'w') as archivo:
            json.dump(usuarios, archivo, indent=4)
        
        print("Usuario registrado correctamente")
        print("--------------------------------------------------------------------------------")
        
        return


    def pedir_contraseña(self):
        contraseña_segura = False
        while not contraseña_segura:
            contraseña = str(getpass.getpass("Introduce contraseña: "))
            contraseña_segura = self._verificar_contraseña(contraseña)
        print("Contraseña segura")
        return contraseña  
    
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
        ...    
            
a = Menus()
a.inicio()
