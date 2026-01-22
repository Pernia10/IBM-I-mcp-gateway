# 🛡️ Secure IBM i MCP Gateway

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/Security-Strict%20Allowlist-red.svg)

**Conecta tu Asistente de IA (Roo Code, Cursor) directamente con tu Mainframe IBM i (AS/400).**

Este gateway permite ejecutar comandos, consultar SQL y compilar programas de forma segura, convirtiendo el lenguaje natural en acciones de sistemas.

---

## ✨ Características Principales

*   **🔒 Seguridad Primero:** Lista blanca estricta (mitigación CWE-78) y encriptación SSH. Bloquea comandos destructivos (`DLT*`, `CLR*`).
*   **⚡ Compilación Inteligente:** Compila **COBOL, RPG y CL** habilitando automáticamente `DBGVIEW(*SOURCE)` para facilitar el debugging.
*   **📂 Navegación sin PDM:** Explora librerías y miembros fuente usando herramientas SQL optimizadas para IA (`list_objects`, `list_members`).
*   **👀 Lectura de Código:** Lee el contenido de miembros fuente directamente desde el chat.

---

## 🚀 Inicio Rápido

### 1. Instalación
```bash
uv sync
cp .env.example .env
```

### 2. Configuración (.env)
```env
IBMI_HOST=YOUR_IBMI_HOST
IBMI_USER=tu_usuario
IBMI_PASS=tu_contraseña
```

### 3. Conexión a Roo Code / Cursor
Agrega esto a tu configuración de MCP (`mcp_settings.json`):

```json
{
  "mcpServers": {
    "ibm-i-gateway": {
      "command": "uv",
      "args": [
        "--directory",
        "RUTA_ABSOLUTA_DEL_PROYECTO",
        "run",
        "ibmi-gateway"
      ]
    }
  }
}
```

---

## 💬 Ejemplos de Uso

| Objetivo | Prompt para la IA |
|----------|-------------------|
| **Monitor** | *"¿Cómo está el uso de CPU y los trabajos activos?"* |
| **Compilar** | *"Compila el programa CUSTUPD en DEVLIB/QCBLLESRC"* |
| **Explorar** | *"Lista todos los programas RPG en la librería PRODLIB"* |
| **Leer** | *"Lee el código del miembro LECTURASQL en SPPLIB"* |
| **SQL** | *"Ejecuta: SELECT * FROM QSYS2.SYSTABLES LIMIT 5"* |

---

## 📚 Documentación Adicional

*   [🔧 Guía de Solución de Problemas (Troubleshooting)](docs/TROUBLESHOOTING.md)
*   [📖 Guía de Uso y Optimización](guia_uso_optimizacion.md)

---
**Author:** Santiago Pernia
