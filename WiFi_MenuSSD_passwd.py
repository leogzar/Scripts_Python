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

def menu_perfiles(perfiles):
    print("\nSeleccione una conexión:")
    for i, perfil in enumerate(perfiles, start=1):
        print(f"{i}. {perfil}")

    opcion = input("\nIngrese el número de la conexión o 'q' para salir: ")
    return opcion.strip()

def obtener_clave_perfil_wifi(nombre_perfil, salida_perfil):
    try:
        # Buscar la sección de "Contenido de la clave" en la salida del perfil
        patron = re.compile(r"Contenido de la clave\s*:\s*(.+)")
        coincidencias = patron.search(salida_perfil)

        if coincidencias:
            clave = coincidencias.group(1).strip()
            return clave

        return None

    except Exception as e:
        print(f"Error al obtener la clave del perfil {nombre_perfil}: {str(e)}")
        return None

# Ejemplo de uso:
comando_windows = "netsh wlan show profiles"
salida_windows, codigo_salida_windows = ejecutar_comando(comando_windows)

if codigo_salida_windows == 0:
    
    # Obtener los nombres de los perfiles
    perfiles_wifi = [linea.split(":")[1].strip() for linea in salida_windows.split('\n') if "Perfil de todos los usuarios" in linea]

    while True:
        opcion_seleccionada = menu_perfiles(perfiles_wifi)

        if opcion_seleccionada.lower() == 'q':
            print("Saliendo del programa.")
            break

        try:
            # Obtener el nombre del perfil seleccionado
            indice_seleccionado = int(opcion_seleccionada) - 1

            if 0 <= indice_seleccionado < len(perfiles_wifi):
                nombre_conexion = perfiles_wifi[indice_seleccionado]

                # Ejecutar el comando 'netsh wlan show profile name="nombre_perfil" key="clear"'
                comando_perfil = f'netsh wlan show profile name="{nombre_conexion}" key="clear"'
                salida_perfil, codigo_salida_perfil = ejecutar_comando(comando_perfil)

                if codigo_salida_perfil == 0:
                    clave_wifi = obtener_clave_perfil_wifi(nombre_conexion, salida_perfil)
                    print(f"\nNombre de la conexión seleccionada: {nombre_conexion}")
                    print(f"Clave de la conexión: {clave_wifi}")
                else:
                    print(f"\nError al obtener el perfil {nombre_conexion}. Código de salida: {codigo_salida_perfil}")
            else:
                print("\nOpción no válida. Por favor, ingrese un número válido.")
        except ValueError:
            print("\nOpción no válida. Por favor, ingrese un número válido.")
elif codigo_salida_windows is not None:
    print(f"Error al ejecutar el comando en Windows. Código de salida: {codigo_salida_windows}")
