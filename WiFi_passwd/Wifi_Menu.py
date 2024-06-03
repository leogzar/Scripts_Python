import os

def ejecutar_script(script):
    try:
        os.system(f"python {script}")
    except Exception as e:
        print(f"Error al ejecutar el script {script}: {e}")

def mostrar_menu():
    print("Seleccione un script para ejecutar:")
    print("1 - WiFi_MenuSSID_passwd")
    print("2 - WiFi_SSID_passwd")
    print("3 - Wifi_SSID_passwd_a_txt")
    print("4 - WiFi_SSID_import")
    print("5 - Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Ingrese el número de opción: ")

        if opcion == "1":
            ejecutar_script("WiFi_MenuSSID_passwd.py")
        elif opcion == "2":
            ejecutar_script("WiFi_SSID_passwd.py")
        elif opcion == "3":
            ejecutar_script("Wifi_SSID_passwd_a_txt.py")
        elif opcion == "4":
            ejecutar_script("WiFi_SSID_import.py")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione un número de opción válido.")

if __name__ == "__main__":
    main()