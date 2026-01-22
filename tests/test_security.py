"""
Pruebas unitarias para validación de seguridad.
"""

import pytest
from ibmi_gateway.security import validate_command, get_security_violation_message


class TestCommandValidation:
    """Casos de prueba para validación de seguridad de comandos."""
    
    def test_allowed_dsp_commands(self):
        """Prueba que los comandos DSP* estén permitidos."""
        assert validate_command("DSPSYSSTS") is True
        assert validate_command("DSPJOB") is True
        assert validate_command("DSPLIBL") is True
    
    def test_allowed_wrk_commands(self):
        """Prueba que los comandos WRK* estén permitidos."""
        assert validate_command("WRKACTJOB") is True
        assert validate_command("WRKSYSSTS") is True
        assert validate_command("WRKOUTQ") is True
    
    def test_allowed_rtv_commands(self):
        """Prueba que los comandos RTV* estén permitidos."""
        assert validate_command("RTVJOBA") is True
        assert validate_command("RTVSYSVAL") is True
    
    def test_allowed_select_queries(self):
        """Prueba que las consultas SQL SELECT estén permitidas."""
        assert validate_command("SELECT * FROM QSYS2.SYSTABLES") is True
        assert validate_command("select column from table limit 10") is True
    
    def test_blocked_delete_commands(self):
        """Prueba que los comandos DLT* estén bloqueados."""
        assert validate_command("DLTLIB TESTLIB") is False
        assert validate_command("DLTF MYFILE") is False
    
    def test_blocked_clear_commands(self):
        """Prueba que los comandos CLR* estén bloqueados."""
        assert validate_command("CLRPFM MYFILE") is False
    
    def test_blocked_change_commands(self):
        """Prueba que los comandos CHG* estén bloqueados."""
        assert validate_command("CHGUSRPRF USER") is False
    
    def test_blocked_call_commands(self):
        """Prueba que los comandos CALL estén bloqueados."""
        assert validate_command("CALL PGM") is False
    
    def test_blocked_command_injection(self):
        """Prueba que los intentos de inyección de comandos estén bloqueados."""
        assert validate_command("DSPSYSSTS; DLTLIB TESTLIB") is False
        assert validate_command("WRKACTJOB | CALL PGM") is False
    
    def test_case_insensitive(self):
        """Prueba que la validación no distinga mayúsculas/minúsculas."""
        assert validate_command("dspsyssts") is True
        assert validate_command("WrKaCtJoB") is True
        assert validate_command("SeLeCt * FrOm TaBle") is True
    
    def test_allowed_compilation_commands(self):
        """Prueba que los comandos de compilación estén permitidos."""
        assert validate_command("CRTBNDCL PGM(MYLIB/MYPGM) SRCFILE(MYLIB/QCLSRC)") is True
        assert validate_command("CRTBNDRPG PGM(MYLIB/MYPGM) SRCFILE(MYLIB/QRPGLESRC)") is True
        assert validate_command("CRTBNDCBL PGM(MYLIB/MYPGM) SRCFILE(MYLIB/QCBLLESRC)") is True
        assert validate_command("CRTSRVPGM SRVPGM(MYLIB/MYSRVPGM)") is True
    
    def test_blocked_other_create_commands(self):
        """Prueba que otros comandos CRT* sigan bloqueados."""
        assert validate_command("CRTUSRPRF USRPRF(HACKER) PASSWORD(BAD)") is False
        assert validate_command("CRTLIB LIB(BADLIB)") is False
        assert validate_command("CRTAUTL AUTL(BADAUTL)") is False
    
    def test_whitespace_handling(self):
        """Prueba que se manejen correctamente los espacios en blanco."""
        assert validate_command("  DSPSYSSTS  ") is True
        assert validate_command("\tWRKACTJOB\n") is True
    
    def test_security_message(self):
        """Prueba que el mensaje de violación de seguridad sea consistente."""
        msg = get_security_violation_message()
        assert "VIOLACIÓN DE SEGURIDAD" in msg
        assert "DSP*" in msg
        assert "WRK*" in msg
        assert "RTV*" in msg
        assert "SELECT" in msg
