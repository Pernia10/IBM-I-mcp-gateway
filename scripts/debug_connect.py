import paramiko
import os
import sys
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("paramiko").setLevel(logging.DEBUG)

load_dotenv()

HOST = os.getenv("IBMI_HOST")
USER = os.getenv("IBMI_USER")
PASS = os.getenv("IBMI_PASS")
PORT = int(os.getenv("IBMI_PORT", 22))

print(f"--- INICIO DE DIAGNÓSTICO ---")
print(f"Destino: {HOST}:{PORT}")
print(f"Usuario: {USER}")
print(f"Longitud de contraseña: {len(PASS) if PASS else 0}")
print(f"-----------------------------")

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print("Iniciando conexión...")
    # Intentar con un timeout más largo para propósitos de depuración
    client.connect(HOST, port=PORT, username=USER, password=PASS, timeout=45, look_for_keys=False, allow_agent=False)
    print("¡Conexión ESTABLECIDA exitosamente!")
    
    print("Probando ejecución de comando (uname)...")
    stdin, stdout, stderr = client.exec_command('uname -a')
    print(f"Salida: {stdout.read().decode().strip()}")
    print(f"Errores: {stderr.read().decode().strip()}")
    
    client.close()
    print("--- DIAGNÓSTICO EXITOSO ---")

except Exception as e:
    print(f"\n!!! CONEXIÓN FALLIDA !!!")
    print(f"Tipo de Error: {type(e).__name__}")
    print(f"Mensaje de Error: {str(e)}")
    print("----------------------------")
    # Para timeouts, podría ser un desajuste de algoritmo
    if "time" in str(e).lower():
        print("SUGERENCIA: El timeout podría indicar bloqueo de Firewall o desajuste de Algoritmo SSH.")
