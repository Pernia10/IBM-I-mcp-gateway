# Secure IBM i MCP Gateway

A professional, security-focused bridge between MCP clients (Cursor, VS Code) and IBM i (AS/400) mainframe systems.

## 🛡️ Security Features

*   **Input Validation:** Strict allowlist preventing command injection (CWE-78)
*   **Allowed Commands:** `DSP*`, `WRK*`, `RTV*`, `SELECT`, `CRTBNDCL`, `CRTBNDRPG`, `CRTBNDCBL`, `CRTSRVPGM`
*   **Blocked Commands:** `DLT*`, `CLR*`, `CHG*`, `CALL`, `CRTUSRPRF`, `CRTLIB`, y otros comandos peligrosos
*   **Encrypted Transport:** SSH (Paramiko) for all communications

## 🛠️ Compilación de Programas

El gateway soporta compilación de programas con debug habilitado por defecto:

*   **COBOL:** Usa `compile_cobol_program` - Compila con `DBGVIEW(*SOURCE)`
*   **RPG/RPGLE:** Usa `compile_rpg_program` - Compila con `DBGVIEW(*SOURCE)`
*   **CL:** Usa `compile_cl_program` - Compila con `DBGVIEW(*SOURCE)`

**Ejemplo de uso con la IA:**
```
"Compila el programa CUSTUPD de DEVLIB/QCBLLESRC"
"Compila ORDRPT de DEVLIB/QRPGLESRC y guárdalo en QGPL"
```

> **Nota:** Todos los programas se compilan con debug habilitado automáticamente para facilitar el desarrollo.

## 🗒️ Navegación Estilo PDM

El gateway incluye herramientas SQL para explorar objetos y miembros (equivalentes modernos a WRKOBJPDM y WRKMBRPDM).

### Listar Objetos
**Herramienta:** `list_library_objects`

**Ejemplo con la IA:**
```
"Muéstrame todos los programas en la biblioteca PRODLIB"
"Lista los archivos (*FILE) en DEVLIB"
```

### Listar Miembros de Source Files
**Herramienta:** `list_source_members`

**Ejemplo con la IA:**
```
"Lista los miembros de DEVLIB/QRPGLESRC ordenados por fecha"
"Cuáles son los últimos 10 programas COBOL modificados en PRODLIB/QCBLLESRC?"
```

**Ventajas sobre PDM tradicional:**
- ✅ Sin necesidad de navegación interactiva
- ✅ La IA puede filtrar y analizar los resultados
- ✅ Combina múltiples consultas automáticamente


## 🚀 Installation

### Prerequisites
- Python 3.12+
- `uv` package manager

### Setup

1. **Clone and navigate to the project:**
   ```powershell
   cd MCP-ibm-i
   ```

2. **Install dependencies:**
   ```powershell
   uv sync
   ```

3. **Configure credentials:**
   Copy `.env.example` to `.env` and fill in your IBM i details:
   ```powershell
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```env
   IBMI_HOST=YOUR_IBMI_HOST
   IBMI_USER=your_username
   IBMI_PASS=your_password
   IBMI_PORT=22
   IBMI_SSH_TIMEOUT=30
   ```

## 🔌 MCP Client Configuration

### For Cursor / Cline

Add to your MCP settings file (e.g., `cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "ibm-i-gateway": {
      "command": "uv",
      "args": [
        "--directory",
        "c:/Users/santiago.pernia/Downloads/MCP-ibm-i",
        "run",
        "ibmi-gateway"
      ]
    }
  }
}
```

> **Note:** Update the path to match your installation directory.

### For VS Code (Alternative)

You can also pass environment variables directly:

```json
{
  "mcpServers": {
    "ibm-i-gateway": {
      "command": "uv",
      "args": ["--directory", "YOUR_PATH", "run", "ibmi-gateway"],
      "env": {
        "IBMI_HOST": "YOUR_IBMI_HOST",
        "IBMI_USER": "username",
        "IBMI_PASS": "password"
      }
    }
  }
}
```

## 🛠️ Usage

### Testing with MCP Inspector

```powershell
npx @modelcontextprotocol/inspector uv run ibmi-gateway
```

This opens a web interface where you can test commands manually.

### Example Commands

**Allowed (Safe):**
- `DSPSYSSTS` - Display system status
- `WRKACTJOB` - Work with active jobs
- `SELECT * FROM QSYS2.SYSTABLES LIMIT 10` - SQL query

**Blocked (Security):**
- `DLTLIB MYLIB` - Delete library (returns security violation)
- `CALL MYPGM` - Call program (returns security violation)

## 🧪 Running Tests

```powershell
uv run pytest tests/ -v
```

## 📁 Project Structure

```
MCP-ibm-i/
├── src/ibmi_gateway/      # Main package
│   ├── server.py          # FastMCP server
│   ├── config.py          # Configuration management
│   ├── security.py        # Command validation
│   └── connection.py      # SSH connection handler
├── scripts/               # Utilities
│   └── debug_connect.py   # Connection diagnostics
├── tests/                 # Unit tests
│   └── test_security.py   # Security tests
├── docs/                  # Documentation
│   └── TROUBLESHOOTING.md # Network diagnostics guide
└── .env                   # Your credentials (gitignored)
```

## 🐛 Troubleshooting

**Connection timeout?** See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) for detailed network diagnostics.

**Quick diagnostic:**
```powershell
uv run scripts/debug_connect.py
```

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

This is a personal project, but suggestions are welcome via issues.
