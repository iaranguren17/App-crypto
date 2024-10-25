import json
import os
import getpass
from criptography import Cripto


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
        
        cripto = Cripto()              #Creamos una clase Cripto
        cripto.desencriptar_json()
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
            option = int(input("Indica operación\n1:Iniciar sesión\n2:Cambiar nombre de registro \n3:Salir\n"))
            while option not in [1,2,3] :
                option= int(input("Por favor, elige una opción correcta: \n"))
            if option == 1:
                cripto.encriptar_json()
                self.login()
            elif option == 2:
                nombre_usuario = str(input("Escribe de nuevo el nombre de usuario: "))
            else:
                cripto.encriptar_json()
                return self.salir()
        
        contraseña = self.pedir_contraseña() #Creamos una contraseña
        salt_usuario = cripto.crear_salt()  #Creamos un salt por usuario
        token_usuario = cripto.crear_token(salt_usuario, contraseña)  #Y el token de la contraseña

        usuarios[nombre_usuario]= {
            "salt": salt_usuario.hex(),
            "token": token_usuario.hex()
        }
        
        with open(ruta_archivo, 'w') as archivo:
            json.dump(usuarios, archivo, indent=4)
        
        cripto.encriptar_json()
        print("Usuario registrado correctamente")
        print("--------------------------------------------------------------------------------")
        
        return False


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
        print("--------------------------------------------------------------------------------")
        print("INICIO DE SESIÓN")
        print("--------------------------------------------------------------------------------")
        cripto = Cripto()
        cripto.desencriptar_json()
        ruta_archivo = os.path.join("Base de datos", "usuarios.json")
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                try:
                    usuarios = json.load(archivo)  
                except json.JSONDecodeError:
                    print("Error al leer la base de datos de usuarios.")
                    return False
        else:
            print("Error con el archivo de usuarios")
            return False
        
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
                cripto.encriptar_json()
                return True
            print("Contraseña incorrecta. Intentos restantes: "+ str(intentos))
            contraseña_usuario = getpass.getpass("Contraseña: ")
            token = cripto.crear_token(salt_usuario, contraseña_usuario )
            token =token.hex()
        cripto.encriptar_json()
        print("Inicio de sesión exitoso")
        return self.pantalla_morosos()
    
    def pantalla_morosos(self):
        ...


            
a = Menus()
a.inicio()
