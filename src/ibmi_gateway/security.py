"""
Módulo de seguridad para validación de comandos.
Implementa estrategias de mitigación CWE-78.
Author: Santiago Pernia
"""

import re


def validate_command(command: str) -> bool:
    """
    CRÍTICO: Mitigación CWE-78
    Valida la entrada contra una lista blanca estricta (DSP*, WRK*, RTV*, SELECT, CRT* específicos).
    Bloquea explícitamente caracteres de inyección como ; y |
    
    Args:
        command: La cadena de comando a validar.
        
    Returns:
        True si el comando es seguro, False en caso contrario.
    """
    # 1. Sanitizar
    command = command.strip().upper()
    
    # 2. Verificar inyección
    if re.search(r'[;|]', command):
        return False

    # 3. Validar contra lista blanca
    allowlist_pattern = r'^(DSP[A-Z0-9]+|WRK[A-Z0-9]+|RTV[A-Z0-9]+|SELECT\s|CRT(BNDCL|BNDRPG|BNDCBL|SRVPGM)\s)'
    
    if re.match(allowlist_pattern, command):
        return True
        
    return False


def get_security_violation_message() -> str:
    """Obtiene el mensaje estándar de violación de seguridad."""
    return "VIOLACIÓN DE SEGURIDAD: Comando bloqueado por Política de Lista Blanca. Permitidos: DSP*, WRK*, RTV*, SELECT, CRTBNDCL, CRTBNDRPG, CRTBNDCBL, CRTSRVPGM."
