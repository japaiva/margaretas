# core/models/__init__.py

"""
Módulo de modelos do Portal de Marketing Margaretas

Este arquivo centraliza todas as importações dos modelos para facilitar
o uso em outras partes do sistema.

Estrutura:
- base.py: Modelos de infraestrutura (Usuario, PerfilUsuario, Parametro)
- cliente.py: Modelos de marketing (Cliente, ProdutoServicoEvento, Campanha)
"""

# ===== IMPORTAÇÕES DA BASE =====
from .base import (
    # Modelos principais
    Usuario,
    PerfilUsuario,
    Parametro,
    
    # Modelos abstratos
    TimeStampedModel,
    AuditedModel,
)

# ===== IMPORTAÇÕES DO CLIENTE/MARKETING =====
from .cliente import (
    # Modelos de marketing
    Cliente,
    ProdutoServicoEvento,
    Campanha,
    
    # Modelo para anexos (se implementado)
    # ClienteAnexo,
    # CampanhaAnexo,
)

# ===== LISTA DE EXPORTAÇÃO =====
__all__ = [
    # === MODELOS BASE ===
    'Usuario',
    'PerfilUsuario', 
    'Parametro',
    'TimeStampedModel',
    'AuditedModel',
    
    # === MODELOS DE MARKETING ===
    'Cliente',
    'ProdutoServicoEvento',
    'Campanha',
    
    # === FUTUROS MODELOS DE ANEXOS ===
    # 'ClienteAnexo',
    # 'CampanhaAnexo',
]

# ===== METADADOS DO MÓDULO =====
__version__ = '1.0.0'
__author__ = 'Portal Margaretas'
__description__ = 'Modelos do Portal de Marketing'

# ===== CONFIGURAÇÕES DJANGO =====
default_app_config = 'core.apps.CoreConfig'