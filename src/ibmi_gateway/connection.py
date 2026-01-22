"""
Gestión de conexión SSH para sistemas IBM i.
Author: Santiago Pernia
"""

import paramiko
from typing import Tuple
from .config import IBMiConfig


class IBMiConnection:
    """Gestiona la conexión SSH al sistema IBM i."""
    
    def __init__(self, config: IBMiConfig):
        """
        Inicializa el gestor de conexión.
        
        Args:
            config: Objeto de configuración IBM i.
        """
        self.config = config
        self.client = None
    
    def connect(self) -> None:
        """Establece una conexión SSH segura al sistema IBM i."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Configuración compatible con IBM i (legacy algorithms)
            transport = self.client.get_transport()
            
            self.client.connect(
                self.config.host,
                port=self.config.port,
                username=self.config.user,
                password=self.config.password,
                timeout=self.config.ssh_timeout,
                look_for_keys=False,
                allow_agent=False,
                banner_timeout=200,
                auth_timeout=200,
                disabled_algorithms={
                    'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256'],
                    'keys': ['rsa-sha2-512', 'rsa-sha2-256']
                },
                gss_auth=False,
                gss_kex=False
            )
        except Exception as e:
            raise RuntimeError(f"Conexión fallida: {str(e)}")
    
    def execute(self, command: str) -> Tuple[str, str]:
        """
        Ejecuta un comando en el sistema IBM i.
        
        Args:
            command: El comando a ejecutar.
            
        Returns:
            Tupla de (stdout, stderr) como strings.
        """
        if not self.client:
            raise RuntimeError("No conectado. Llama a connect() primero.")
        
        # Envuelve comandos CL con la utilidad 'system' para ejecución apropiada
        cmd_to_run = command
        if not command.upper().startswith("SELECT"):
            cmd_to_run = f'system "{command}"'
        
        stdin, stdout, stderr = self.client.exec_command(cmd_to_run)
        
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        return output, error
    
    def close(self) -> None:
        """Cierra la conexión SSH."""
        if self.client:
            self.client.close()
            self.client = None
    
    def __enter__(self):
        """Entrada del context manager."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Salida del context manager."""
        self.close()
