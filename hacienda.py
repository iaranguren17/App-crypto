class Menus():
    
    @staticmethod
    def inicio():

        print("\n BIENVENIDO, CAZADOR DE MOROSOS")
        accion = int(input("\nSelecciona una opción: \n1-Registrarse \n2-Iniciar sesión \n3-Salir\nIntroduce el número de la acción: "))

        if accion == 1:
            Menus.registrase()
        elif accion == 2:
            Menus.login()
        elif accion == 3:
            print("\nMuchas gracias, hasta la próxima\nFIN DE PROGRAMA") 

    def registrarse(self):
        ...

a = Menus()
a.inicio()
