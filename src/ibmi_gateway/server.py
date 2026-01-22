"""
Servidor FastMCP para IBM i Gateway.
"""

from mcp.server.fastmcp import FastMCP
from .config import IBMiConfig
from .connection import IBMiConnection
from .security import validate_command, get_security_violation_message

# Inicializar FastMCP
mcp = FastMCP("Secure IBM i Gateway")


@mcp.tool()
def execute_system_command(command: str) -> str:
    """
    Ejecuta un comando CL o consulta SQL en el sistema IBM i de forma segura.
    
    Args:
        command: La cadena de comando CL o consulta SQL (ej., 'WRKACTJOB', 'SELECT * FROM LIB.TABLE')
        
    Returns:
        La salida del comando o un mensaje de violación de seguridad.
    """
    # 1. Verificación de Seguridad
    if not validate_command(command):
        return get_security_violation_message()

    # 2. Cargar Configuración
    try:
        config = IBMiConfig.from_env()
    except ValueError as e:
        return f"Error de Configuración: {str(e)}"

    # 3. Ejecutar Comando
    try:
        with IBMiConnection(config) as conn:
            output, error = conn.execute(command)
            
            if error:
                return f"Error: {error}"
                
            return output

    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def compile_cobol_program(
    source_library: str,
    source_file: str,
    member: str,
    target_library: str = None,
    program_name: str = None
) -> str:
    """
    Compila un programa COBOL con debug habilitado.
    
    Args:
        source_library: Biblioteca donde está el source (ej. 'DEVLIB')
        source_file: Archivo fuente (ej. 'QCBLLESRC')
        member: Nombre del miembro a compilar
        target_library: Biblioteca destino (default: source_library)
        program_name: Nombre del programa compilado (default: member)
        
    Returns:
        Resultado de la compilación con mensajes de error si hay.
    """
    # Valores por defecto
    target_lib = target_library or source_library
    pgm_name = program_name or member
    
    # Construir comando de compilación con debug habilitado
    command = (
        f"CRTBNDCBL PGM({target_lib}/{pgm_name}) "
        f"SRCFILE({source_library}/{source_file}) "
        f"SRCMBR({member}) "
        f"DBGVIEW(*SOURCE) "
        f"OPTION(*EVENTF) "
        f"TEXT('Compilado con debug habilitado')"
    )
    
    # Validar seguridad
    if not validate_command(command):
        return get_security_violation_message()
    
    # Cargar configuración
    try:
        config = IBMiConfig.from_env()
    except ValueError as e:
        return f"Error de Configuración: {str(e)}"
    
    # Ejecutar compilación
    try:
        with IBMiConnection(config) as conn:
            output, error = conn.execute(command)
            
            if error:
                return f"Error de Compilación: {error}"
                
            return f"Compilación exitosa de {pgm_name} en {target_lib}\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def compile_rpg_program(
    source_library: str,
    source_file: str,
    member: str,
    target_library: str = None,
    program_name: str = None
) -> str:
    """
    Compila un programa RPG/RPGLE con debug habilitado.
    
    Args:
        source_library: Biblioteca donde está el source (ej. 'DEVLIB')
        source_file: Archivo fuente (ej. 'QRPGLESRC')
        member: Nombre del miembro a compilar
        target_library: Biblioteca destino (default: source_library)
        program_name: Nombre del programa compilado (default: member)
        
    Returns:
        Resultado de la compilación con mensajes de error si hay.
    """
    # Valores por defecto
    target_lib = target_library or source_library
    pgm_name = program_name or member
    
    # Construir comando de compilación con debug habilitado
    command = (
        f"CRTBNDRPG PGM({target_lib}/{pgm_name}) "
        f"SRCFILE({source_library}/{source_file}) "
        f"SRCMBR({member}) "
        f"DBGVIEW(*SOURCE) "
        f"OPTION(*EVENTF) "
        f"TEXT('Compilado con debug habilitado')"
    )
    
    # Validar seguridad
    if not validate_command(command):
        return get_security_violation_message()
    
    # Cargar configuración
    try:
        config = IBMiConfig.from_env()
    except ValueError as e:
        return f"Error de Configuración: {str(e)}"
    
    # Ejecutar compilación
    try:
        with IBMiConnection(config) as conn:
            output, error = conn.execute(command)
            
            if error:
                return f"Error de Compilación: {error}"
                
            return f"Compilación exitosa de {pgm_name} en {target_lib}\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def compile_cl_program(
    source_library: str,
    source_file: str,
    member: str,
    target_library: str = None,
    program_name: str = None
) -> str:
    """
    Compila un programa CL con debug habilitado.
    
    Args:
        source_library: Biblioteca donde está el source (ej. 'DEVLIB')
        source_file: Archivo fuente (ej. 'QCLSRC')
        member: Nombre del miembro a compilar
        target_library: Biblioteca destino (default: source_library)
        program_name: Nombre del programa compilado (default: member)
        
    Returns:
        Resultado de la compilación con mensajes de error si hay.
    """
    # Valores por defecto
    target_lib = target_library or source_library
    pgm_name = program_name or member
    
    # Construir comando de compilación con debug habilitado
    command = (
        f"CRTBNDCL PGM({target_lib}/{pgm_name}) "
        f"SRCFILE({source_library}/{source_file}) "
        f"SRCMBR({member}) "
        f"DBGVIEW(*SOURCE) "
        f"TEXT('Compilado con debug habilitado')"
    )
    
    # Validar seguridad
    if not validate_command(command):
        return get_security_violation_message()
    
    # Cargar configuración
    try:
        config = IBMiConfig.from_env()
    except ValueError as e:
        return f"Error de Configuración: {str(e)}"
    
    # Ejecutar compilación
    try:
        with IBMiConnection(config) as conn:
            output, error = conn.execute(command)
            
            if error:
                return f"Error de Compilación: {error}"
                
            return f"Compilación exitosa de {pgm_name} en {target_lib}\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def list_library_objects(
    library: str,
    object_type: str = "*ALL"
) -> str:
    """
    Lista objetos en una biblioteca (equivalente a WRKOBJPDM).
    
    Args:
        library: Nombre de la biblioteca a consultar
        object_type: Tipo de objeto a filtrar (*ALL, *PGM, *FILE, *DTAARA, etc.)
        
    Returns:
        Lista formateada de objetos con nombre, tipo, texto descriptivo y fecha de creación.
    """
    # Construir consulta SQL usando Db2 for i Services
    type_filter = "" if object_type == "*ALL" else f" AND OBJTYPE = '{object_type.replace('*', '')}'"
    
    query = f"""
        SELECT OBJNAME, OBJTYPE, OBJTEXT, 
               VARCHAR_FORMAT(OBJCREATED, 'YYYY-MM-DD HH24:MI:SS') AS CREATED
        FROM TABLE(QSYS2.OBJECT_STATISTICS('{library}', '*ALL'))
        WHERE OBJTYPE IS NOT NULL{type_filter}
        ORDER BY OBJNAME
        FETCH FIRST 100 ROWS ONLY
    """
    
    # Validar seguridad (SELECT ya está permitido)
    if not validate_command(query):
        return get_security_violation_message()
    
    # Ejecutar consulta
    try:
        config = IBMiConfig.from_env()
        with IBMiConnection(config) as conn:
            output, error = conn.execute(query)
            
            if error:
                return f"Error al consultar objetos: {error}"
            
            if not output.strip():
                return f"No se encontraron objetos en la biblioteca {library}."
            
            return f"Objetos en {library} (Tipo: {object_type}):\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def list_source_members(
    library: str,
    source_file: str
) -> str:
    """
    Lista miembros de un source file (equivalente a WRKMBRPDM).
    
    Args:
        library: Biblioteca que contiene el source file
        source_file: Nombre del source file (ej. QRPGLESRC, QCBLLESRC)
        
    Returns:
        Lista de miembros con nombre, tipo de source, descripción y última modificación.
    """
    # Consulta SQL para obtener miembros
    query = f"""
        SELECT SYSTEM_TABLE_MEMBER AS MEMBER,
               SOURCE_TYPE,
               PARTITION_TEXT AS TEXT,
               VARCHAR_FORMAT(LAST_CHANGE_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS') AS LAST_CHANGED
        FROM QSYS2.SYSPARTITIONSTAT
        WHERE SYSTEM_TABLE_SCHEMA = '{library}'
          AND SYSTEM_TABLE_NAME = '{source_file}'
        ORDER BY LAST_CHANGE_TIMESTAMP DESC
        FETCH FIRST 100 ROWS ONLY
    """
    
    # Validar seguridad
    if not validate_command(query):
        return get_security_violation_message()
    
    # Ejecutar consulta
    try:
        config = IBMiConfig.from_env()
        with IBMiConnection(config) as conn:
            output, error = conn.execute(query)
            
            if error:
                return f"Error al consultar miembros: {error}"
            
            if not output.strip():
                return f"No se encontraron miembros en {library}/{source_file}."
            
            return f"Miembros en {library}/{source_file} (ordenados por fecha):\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


@mcp.tool()
def read_source_member(
    library: str,
    source_file: str,
    member: str
) -> str:
    """
    Lee el contenido completo de un miembro de source file (código fuente).
    
    Args:
        library: Biblioteca que contiene el source file
        source_file: Nombre del source file (ej. QRPGLESRC, QCBLLESRC, PRUCBL)
        member: Nombre del miembro a leer (ej. LECTURASQL)
        
    Returns:
        Contenido del código fuente con números de línea.
    """
    # Consulta SQL usando la función QSYS2.SOURCE_FILE_CONTENTS
    query = f"""
        SELECT SRCSEQ, SRCDTA
        FROM TABLE(
            QSYS2.SOURCE_FILE_CONTENTS(
                SOURCE_FILE => '{source_file}',
                SOURCE_LIBRARY => '{library}',
                SOURCE_MEMBER => '{member}'
            )
        )
        ORDER BY SRCSEQ
    """
    
    # Validar seguridad
    if not validate_command(query):
        return get_security_violation_message()
    
    # Ejecutar consulta
    try:
        config = IBMiConfig.from_env()
        with IBMiConnection(config) as conn:
            output, error = conn.execute(query)
            
            if error:
                return f"Error al leer el miembro: {error}"
            
            if not output.strip():
                return f"El miembro {library}/{source_file}.{member} está vacío o no existe."
            
            return f"Código fuente de {library}/{source_file}.{member}:\n{output}"
    
    except Exception as e:
        return f"Error de Ejecución: {str(e)}"


def main():
    """Punto de entrada para el servidor."""
    mcp.run()


if __name__ == "__main__":
    main()
