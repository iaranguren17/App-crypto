from criptography import Cripto
import os
import json
class ki():
    def Interrupt(self, b):
        print("\nPrograma interrumpido")
        
        if b == 1:   
            ruta_usuarios = os.path.join("Base de datos", "usuarios.json")
            with open(ruta_usuarios, 'r') as archivo:
                usuarios =  json.load(archivo)
            
            if  isinstance(usuarios, dict):
                cripto = Cripto()
                cripto.encriptar_json_usuarios()

        elif b ==2:
            ruta_morosos = os.path.join("Base de datos", "morosos.json")
            with open(ruta_morosos, 'r') as archivo:
                morosos =  json.load(archivo)
            if isinstance(morosos, dict):
                cripto = Cripto()   
                cripto.encriptar_json_morosos()
        print("Programa Cerrado")
        exit(1)