# gestor/views/__init__.py

# Views do dashboard
from .dashboard import (
    home,
    dashboard,
    configuracoes,
    parametro_list,
    parametro_create,
    parametro_update,
    relatorios,
    relatorio_clientes,
    relatorio_campanhas,
    relatorio_performance,
)

# Views do usuário
from .usuario import (
    usuario_list,
    usuario_create,
    usuario_detail,
    usuario_update,
    usuario_delete,
    usuario_perfil,
)

# Views do cliente - ATUALIZADAS (sem produto/serviço)
from .cliente import (
    # Cliente CRUD
    cliente_list,
    cliente_detail,
    cliente_create,
    cliente_update,
    cliente_delete,
    cliente_checklist,
    
    # Campanha CRUD
    campanha_list,
    campanha_detail,
    campanha_create,
    campanha_update,
    campanha_delete,
    campanha_change_status,
    
    # APIs
    cliente_api_search,
    cliente_api_stats,
    
    # Wizard
    cliente_wizard,
)

# Views do wizard
from .cliente_wizard import (
    ClienteWizardView,
)

# Lista do que pode ser importado com "from gestor.views import *"
__all__ = [
    # Dashboard
    'home', 'dashboard', 'configuracoes', 'parametro_list', 'parametro_create',
    'parametro_update', 'relatorios', 'relatorio_clientes', 'relatorio_campanhas',
    'relatorio_performance',
    
    # Usuário
    'usuario_list', 'usuario_create', 'usuario_detail', 'usuario_update',
    'usuario_delete', 'usuario_perfil',
    
    # Cliente
    'cliente_list', 'cliente_detail', 'cliente_create', 'cliente_update',
    'cliente_delete', 'cliente_checklist',
    
    # Campanha
    'campanha_list', 'campanha_detail', 'campanha_create', 'campanha_update',
    'campanha_delete', 'campanha_change_status',
    
    # APIs e Wizard
    'cliente_api_search', 'cliente_api_stats', 'cliente_wizard', 'ClienteWizardView',
]