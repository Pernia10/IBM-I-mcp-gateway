"""
Secure IBM i MCP Gateway

Un puente seguro entre clientes MCP y sistemas IBM i (AS/400).
"""

__version__ = "0.1.0"
__author__ = "Santiago Pernia"

from .server import mcp

__all__ = ["mcp"]
