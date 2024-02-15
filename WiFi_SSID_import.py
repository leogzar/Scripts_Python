import subprocess
import os

def ejecutar_comando(command):
    try:
        # Ejecutar el comando y capturar la salida
        resultado = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # Devolver la salida estándar y el código de salida
        return resultado.stdout, resultado.returncode

    except Exception as e:
        print(f"Error al ejecutar el comando: {str(e)}")
        return None, None

def importar_perfiles_wifi(archivo):
    with open(archivo, "r") as archivo_txt:
        lineas = archivo_txt.readlines()

    for linea in lineas[4:]:
        # Si la línea no está vacía y no es una línea de comentario
        if linea.strip() and not linea.startswith("#"):
            # Dividir la línea en perfil y clave
            datos = linea.strip().split("[")
            perfil = datos[1].split("]")[0].strip()
            clave = datos[2].split("]")[0].strip()
            generar_perfil_wifi(perfil, clave)  # Generar perfil WiFi

def generar_perfil_wifi(perfil, clave):
    # Generar XML para el perfil WiFi
    nombre_archivo_temporal = f"{perfil}.xml"
    with open(nombre_archivo_temporal, "w") as archivo_temporal:
        archivo_temporal.write('<?xml version="1.0"?>\n')
        archivo_temporal.write('<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n')
        archivo_temporal.write(f'    <name>{perfil}</name>\n')
        archivo_temporal.write('    <SSIDConfig>\n')
        archivo_temporal.write('        <SSID>\n')
        archivo_temporal.write(f'            <name>{perfil}</name>\n')
        archivo_temporal.write('        </SSID>\n')
        archivo_temporal.write('    </SSIDConfig>\n')
        archivo_temporal.write('    <connectionType>ESS</connectionType>\n')
        archivo_temporal.write('    <connectionMode>auto</connectionMode>\n')
        archivo_temporal.write('    <MSM>\n')
        archivo_temporal.write('        <security>\n')
        archivo_temporal.write('            <authEncryption>\n')
        archivo_temporal.write('                <authentication>WPA2PSK</authentication>\n')
        archivo_temporal.write('                <encryption>AES</encryption>\n')
        archivo_temporal.write('                <useOneX>false</useOneX>\n')
        archivo_temporal.write('            </authEncryption>\n')
        archivo_temporal.write('            <sharedKey>\n')
        archivo_temporal.write('                <keyType>passPhrase</keyType>\n')
        archivo_temporal.write('                <protected>false</protected>\n')
        archivo_temporal.write(f'                <keyMaterial>{clave}</keyMaterial>\n')
        archivo_temporal.write('            </sharedKey>\n')
        archivo_temporal.write('        </security>\n')
        archivo_temporal.write('    </MSM>\n')
        archivo_temporal.write('</WLANProfile>\n')

    # Comando para importar el perfil WiFi a Windows
    comando = f'netsh wlan add profile filename="{nombre_archivo_temporal}" user=all'
    salida, codigo_salida = ejecutar_comando(comando)

    if codigo_salida == 0:
        print(f"Perfil WiFi '{perfil}' agregado correctamente.")
    else:
        print(f"Error al agregar el perfil WiFi '{perfil}'. Código de salida: {codigo_salida}")
        if salida:
            print("Mensaje de salida:", salida)

    # Eliminar el archivo temporal
    os.remove(nombre_archivo_temporal)

# Importar perfiles WiFi desde el archivo wifi_ssid_passwd.txt
importar_perfiles_wifi("wifi_ssid_passwd.txt")