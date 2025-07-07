# gestor/views/__init__.py - VERSÃO CORRIGIDA BASEADA NOS ARQUIVOS EXISTENTES

# ===== VIEWS DE DASHBOARD =====
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
    relatorio_performance
)

# ===== VIEWS DE USUÁRIO =====
from .usuario import (
    usuario_list,
    usuario_perfil,
    usuario_create,
    usuario_detail,
    usuario_update,
    usuario_delete
)

# ===== VIEWS DE CLIENTE =====
from .cliente import (
    # Views principais
    cliente_list,
    cliente_detail,
    cliente_create,
    cliente_update,
    cliente_delete,
    
    # Checklist
    cliente_checklist,
    cliente_checklist_update,
    
    # Briefing
    cliente_briefing,
    
    # API
    cliente_api_search,
    cliente_api_stats,
)

# ===== VIEWS DE WIZARD =====
from .cliente_wizard import (
    ClienteWizardView,
)

# ===== VIEWS DE PRODUTOS/SERVIÇOS =====
# Nota: Arquivo se chama cliente_produto_servico.py (não cliente_produtos_servicos.py)
from .cliente_produto_servico import (
    # Views inline
    produto_servico_create_inline,
    produto_servico_update_inline,
    produto_servico_delete_inline,
    produto_servico_toggle_status_inline,
    
    # Views de resposta rápida
    produto_servico_quick_create,
    
    # Relatórios e estatísticas
    cliente_produtos_servicos_stats,
    produto_servico_api_search_cliente,
)

# ===== VIEWS DE CAMPANHAS =====
from .cliente_campanhas import (
    # Views principais
    campanha_list,
    campanha_detail,
    campanha_create,
    campanha_update,
    campanha_delete,
    campanha_change_status,
    
    # Views inline
    campanha_create_inline,
    campanha_update_inline,
    campanha_delete_inline,
    
    # API
    campanha_api_search,
    cliente_campanhas_stats,
)

# ===== MANTER COMPATIBILIDADE =====
__all__ = [
    # Dashboard
    'home',
    'dashboard',
    'configuracoes',
    'parametro_list',
    'parametro_create', 
    'parametro_update',
    'relatorios',
    'relatorio_clientes',
    'relatorio_campanhas',
    'relatorio_performance',
    
    # Usuário
    'usuario_list',
    'usuario_perfil',
    'usuario_create',
    'usuario_detail',
    'usuario_update',
    'usuario_delete',
    
    # Cliente
    'cliente_list',
    'cliente_detail', 
    'cliente_create',
    'cliente_update',
    'cliente_delete',
    'cliente_checklist',
    'cliente_checklist_update',
    'cliente_briefing',
    'cliente_api_search',
    'cliente_api_stats',
    
    # Wizard
    'ClienteWizardView',
    
    # Produtos/Serviços inline
    'produto_servico_create_inline',
    'produto_servico_update_inline',
    'produto_servico_delete_inline',
    'produto_servico_toggle_status_inline',
    'produto_servico_quick_create',
    'cliente_produtos_servicos_stats',
    'produto_servico_api_search_cliente',
    
    # Campanhas
    'campanha_list',
    'campanha_detail',
    'campanha_create',
    'campanha_update',
    'campanha_delete',
    'campanha_change_status',
    'campanha_create_inline',
    'campanha_update_inline', 
    'campanha_delete_inline',
    'campanha_api_search',
    'cliente_campanhas_stats',
]