import subprocess
import re

def ejecutar_comando(command):
    try:
        # Ejecutar el comando y capturar la salida
        resultado = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # Devolver la salida estándar y el código de salida
        return resultado.stdout, resultado.returncode

    except Exception as e:
        print(f"Error al ejecutar el comando: {str(e)}")
        return None, None

def obtener_perfiles_wifi(exportar=False):
    comando = "netsh wlan show profiles"
    salida, codigo_salida = ejecutar_comando(comando)

    if codigo_salida == 0:
        perfiles_wifi = [linea.split(":")[1].strip() for linea in salida.split('\n') if "Perfil de todos los usuarios" in linea]

        if exportar:
            with open("wifi_ssid_passwd.txt", "w") as archivo:
                archivo.write("################################\n")
                archivo.write("#Listado de perfiles y claves: #\n")
                archivo.write("################################\n")
                archivo.write("{:<20} {:<20}\n".format("Perfil WiFi", "passwd"))
                for perfil in perfiles_wifi:
                    clave = obtener_clave_perfil_wifi(perfil)
                    if clave is not None:
                        archivo.write("{:<20} {:<20}\n".format(perfil, clave))

        return perfiles_wifi
    else:
        print(f"Error al obtener perfiles de WiFi. Código de salida: {codigo_salida}")
        return []

def obtener_clave_perfil_wifi(nombre_perfil):
    comando = f'netsh wlan show profile name="{nombre_perfil}" key="clear"'
    salida, codigo_salida = ejecutar_comando(comando)

    if codigo_salida == 0:
        # Buscar la línea que contiene la clave
        patron = re.compile(r"Contenido de la clave\s*:\s*(.+)")
        coincidencias = patron.search(salida)

        if coincidencias:
            clave = coincidencias.group(1).strip()
            return clave
        else:
            return None
    else:
        print(f"Error al obtener la clave del perfil {nombre_perfil}. Código de salida: {codigo_salida}")
        return None

# Obtener los perfiles de WiFi
perfiles_wifi = obtener_perfiles_wifi()

if perfiles_wifi:
    print("################################")
    print("#Listado de perfiles y claves: #")
    print("################################")
    print("{:<20} {:<20}".format("Perfil WiFi:", "Passwd:"))
    for nombre_perfil in perfiles_wifi:
        clave_wifi = obtener_clave_perfil_wifi(nombre_perfil)
        if clave_wifi is not None:
            print("{:<20} {:<20}".format(nombre_perfil, clave_wifi))
    
    opcion = input("\nPresione 'x' para exportar a un archivo txt, o 'q' para salir: ")
    if opcion.lower() == 'x':
        obtener_perfiles_wifi(exportar=True)
        print("Perfiles y claves exportados en wifi_ssid_passwd.txt")
    elif opcion.lower() == 'q':
        print("Saliendo del programa.")
else:
    print("\nNo se encontraron perfiles de WiFi.")
