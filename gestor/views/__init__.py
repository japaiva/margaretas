# gestor/views/__init__.py

# Importar todas as views dos módulos para que possam ser acessadas via import

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

# Views do cliente
from .cliente import (
    cliente_list,
    cliente_detail,
    cliente_create,
    cliente_update,
    cliente_delete,
    cliente_wizard_step2,
    cliente_wizard_step3,
    cliente_wizard_step4,
    cliente_wizard_step5,
    cliente_wizard_step6,
    produto_servico_list,
    produto_servico_create,
    produto_servico_detail,
    produto_servico_update,
    produto_servico_delete,
    campanha_list,
    campanha_detail,
    campanha_create,
    campanha_update,
    campanha_delete,
    cliente_api_search,
    produto_servico_api_by_cliente,
    cliente_form_htmx,
    campanha_form_htmx,
)

# Definir what pode ser importado quando usar "from gestor.views import *"
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
    'usuario_create',
    'usuario_detail',
    'usuario_update',
    'usuario_delete',
    'usuario_perfil',
    
    # Cliente
    'cliente_list',
    'cliente_detail',
    'cliente_create',
    'cliente_update',
    'cliente_delete',
    'cliente_wizard_step2',
    'cliente_wizard_step3',
    'cliente_wizard_step4',
    'cliente_wizard_step5',
    'cliente_wizard_step6',
    'produto_servico_list',
    'produto_servico_create',
    'produto_servico_detail',
    'produto_servico_update',
    'produto_servico_delete',
    'campanha_list',
    'campanha_detail',
    'campanha_create',
    'campanha_update',
    'campanha_delete',
    'cliente_api_search',
    'produto_servico_api_by_cliente',
    'cliente_form_htmx',
    'campanha_form_htmx',
]