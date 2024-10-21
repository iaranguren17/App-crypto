#Este es el main bueno
import json
import os
import getpass

class Menu:
    def __init__(self):
        # No es necesario inicializar nada si no hay atributos, pero este método es necesario para instanciar la clase.
        pass
    
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

# Instancia de la clase y llamada al método
a = Menu()
a.pedir_contraseña()
