"""
Módulo de seguridad para validación de comandos.
Implementa estrategias de mitigación CWE-78.
"""

import re


def validate_command(command: str) -> bool:
    """
    CRÍTICO PARA SEGURIDAD: Mitigación CWE-78
    Valida la entrada contra una lista blanca estricta de comandos benignos.
    Previene Inyección de Comandos rechazando cualquier comando no permitido explícitamente.
    
    Lista Blanca:
    - DSP* (Comandos Display)
    - WRK* (Comandos Work with)
    - RTV* (Comandos Retrieve)
    - SELECT (SQL solo lectura)
    
    Lista Negra (Implícita):
    - DLT* (Delete)
    - CLR* (Clear)
    - CHG* (Change)
    - CALL (Ejecutar programas)
    - RM, MV, CP (Comandos tipo Unix)
    - ; (Encadenamiento de comandos)
    - | (Piping)
    
    Args:
        command: La cadena de comando a validar.
        
    Returns:
        True si el comando es seguro, False en caso contrario.
    """
    # 1. Sanitizar: Eliminar espacios al inicio/final
    command = command.strip().upper()
    
    # 2. Verificar caracteres peligrosos (Encadenamiento/Inyección de Comandos)
    # El regex verifica punto y coma o caracteres pipe que podrían permitir ejecutar comandos arbitrarios
    if re.search(r'[;|]', command):
        return False

    # 3. Patrón Regex de Lista Blanca
    # Solo permite comandos que empiecen con DSP, WRK, RTV, SELECT, o comandos de compilación específicos
    # Comandos de compilación permitidos: CRTBNDCL, CRTBNDRPG, CRTBNDCBL, CRTSRVPGM
    # El patrón asegura que el comando comience con una de estas palabras clave
    allowlist_pattern = r'^(DSP[A-Z0-9]+|WRK[A-Z0-9]+|RTV[A-Z0-9]+|SELECT\s|CRT(BNDCL|BNDRPG|BNDCBL|SRVPGM)\s)'
    
    if re.match(allowlist_pattern, command):
        return True
        
    return False


def get_security_violation_message() -> str:
    """Obtiene el mensaje estándar de violación de seguridad."""
    return "VIOLACIÓN DE SEGURIDAD: Comando bloqueado por Política de Lista Blanca. Permitidos: DSP*, WRK*, RTV*, SELECT, CRTBNDCL, CRTBNDRPG, CRTBNDCBL, CRTSRVPGM."
