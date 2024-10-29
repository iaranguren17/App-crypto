import os
from hacienda import Menus
from criptography import Cripto
from keyboardInterrupt import ki
def main():
    menu = Menus()
    try:
        menu.inicio()
    except KeyboardInterrupt:
        a = ki()
        a.Interrupt()

if __name__== "__main__":
    main()