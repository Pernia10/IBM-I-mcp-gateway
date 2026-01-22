"""
Gestión de configuración para IBM i Gateway.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class IBMiConfig:
    """Configuración para la conexión IBM i."""
    
    host: str
    user: str
    password: str
    port: int = 22
    ssh_timeout: int = 30
    
    @classmethod
    def from_env(cls) -> 'IBMiConfig':
        """Carga la configuración desde variables de entorno."""
        load_dotenv()
        
        host = os.getenv("IBMI_HOST")
        user = os.getenv("IBMI_USER")
        password = os.getenv("IBMI_PASS")
        port = int(os.getenv("IBMI_PORT", 22))
        ssh_timeout = int(os.getenv("IBMI_SSH_TIMEOUT", 30))
        
        if not all([host, user, password]):
            raise ValueError(
                "Faltan variables de entorno requeridas. "
                "Por favor configura IBMI_HOST, IBMI_USER, y IBMI_PASS en tu archivo .env."
            )
        
        return cls(
            host=host,
            user=user,
            password=password,
            port=port,
            ssh_timeout=ssh_timeout
        )
