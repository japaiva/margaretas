# core/models/__init__.py

"""
Módulo de modelos do Portal de Marketing Margaretas

Estrutura:
- base.py: Modelos de infraestrutura (Usuario, PerfilUsuario, Parametro)
- cliente.py: Modelos de marketing (Cliente, ClienteChecklist, Campanha)
"""

# ===== IMPORTAÇÕES DA BASE =====
from .base import (
    Usuario,
    PerfilUsuario,
    Parametro,
    TimeStampedModel,
    AuditedModel,
)

# ===== IMPORTAÇÕES DO CLIENTE/MARKETING =====
from .cliente import (
    Cliente,
    ClienteChecklist,
    Campanha,
)

# ===== LISTA DE EXPORTAÇÃO =====
__all__ = [
    # Modelos base
    'Usuario',
    'PerfilUsuario', 
    'Parametro',
    'TimeStampedModel',
    'AuditedModel',
    
    # Modelos de marketing
    'Cliente',
    'ClienteChecklist',
    'Campanha',
]