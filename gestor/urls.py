# gestor/urls.py - VERSÃO COM IMPORT ESPECÍFICO

from django.urls import path

# Import específico de cada função para evitar conflitos
from .views.dashboard import (
    home, dashboard, configuracoes, parametro_list, 
    parametro_create, parametro_update, relatorios,
    relatorio_clientes, relatorio_campanhas, relatorio_performance
)
from .views import usuario, cliente

app_name = 'gestor'

urlpatterns = [
    # ===== PÁGINAS PRINCIPAIS =====
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # ===== CLIENTE DE MARKETING =====
    path('clientes/', cliente.cliente_list, name='cliente_list'),
    path('clientes/novo/', cliente.cliente_create, name='cliente_create'),
    path('clientes/<uuid:pk>/', cliente.cliente_detail, name='cliente_detail'),
    path('clientes/<uuid:pk>/editar/', cliente.cliente_update, name='cliente_update'),
    path('clientes/<uuid:pk>/excluir/', cliente.cliente_delete, name='cliente_delete'),
    
    # ===== WIZARD DE CLIENTE =====
    path('clientes/<uuid:pk>/step1/', cliente.cliente_wizard_step1, name='cliente_wizard_step1'),
    path('clientes/<uuid:pk>/step2/', cliente.cliente_wizard_step2, name='cliente_wizard_step2'),
    path('clientes/<uuid:pk>/step3/', cliente.cliente_wizard_step3, name='cliente_wizard_step3'),
    path('clientes/<uuid:pk>/step4/', cliente.cliente_wizard_step4, name='cliente_wizard_step4'),
    path('clientes/<uuid:pk>/step5/', cliente.cliente_wizard_step5, name='cliente_wizard_step5'),
    path('clientes/<uuid:pk>/step6/', cliente.cliente_wizard_step6, name='cliente_wizard_step6'),
    
    # ===== PRODUTOS/SERVIÇOS/EVENTOS =====
    path('clientes/<uuid:cliente_id>/produtos/', cliente.produto_servico_list, name='produto_servico_list'),
    path('clientes/<uuid:cliente_id>/produtos/novo/', cliente.produto_servico_create, name='produto_servico_create'),
    path('produtos/<uuid:pk>/', cliente.produto_servico_detail, name='produto_servico_detail'),
    path('produtos/<uuid:pk>/editar/', cliente.produto_servico_update, name='produto_servico_update'),
    path('produtos/<uuid:pk>/excluir/', cliente.produto_servico_delete, name='produto_servico_delete'),
    
    # ===== CAMPANHAS =====
    path('campanhas/', cliente.campanha_list, name='campanha_list'),
    path('campanhas/nova/', cliente.campanha_create, name='campanha_create'),
    path('campanhas/<uuid:pk>/', cliente.campanha_detail, name='campanha_detail'),
    path('campanhas/<uuid:pk>/editar/', cliente.campanha_update, name='campanha_update'),
    path('campanhas/<uuid:pk>/excluir/', cliente.campanha_delete, name='campanha_delete'),
    
    # ===== USUÁRIOS =====
    path('usuarios/', usuario.usuario_list, name='usuario_list'),
    path('usuarios/novo/', usuario.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/', usuario.usuario_detail, name='usuario_detail'),
    path('usuarios/<int:pk>/editar/', usuario.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', usuario.usuario_delete, name='usuario_delete'),
    path('usuarios/<int:pk>/perfil/', usuario.usuario_perfil, name='usuario_perfil'),
    
    # ===== CONFIGURAÇÕES =====
    path('configuracoes/', configuracoes, name='configuracoes'),
    path('parametros/', parametro_list, name='parametro_list'),
    path('parametros/novo/', parametro_create, name='parametro_create'),
    path('parametros/<int:pk>/editar/', parametro_update, name='parametro_update'),
    
    # ===== APIs INTERNAS =====
    path('api/clientes/search/', cliente.cliente_api_search, name='api_cliente_search'),
    path('api/produtos-servicos/<uuid:cliente_id>/', cliente.produto_servico_api_by_cliente, name='api_produto_servico_by_cliente'),
    
    # ===== RELATÓRIOS =====
    path('relatorios/', relatorios, name='relatorios'),
    path('relatorios/clientes/', relatorio_clientes, name='relatorio_clientes'),
    path('relatorios/campanhas/', relatorio_campanhas, name='relatorio_campanhas'),
    path('relatorios/performance/', relatorio_performance, name='relatorio_performance'),
    
    # ===== AJAX/HTMX =====
    path('htmx/cliente-form/', cliente.cliente_form_htmx, name='htmx_cliente_form'),
    path('htmx/campanha-form/', cliente.campanha_form_htmx, name='htmx_campanha_form'),
]