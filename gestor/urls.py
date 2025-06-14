# gestor/urls.py - VERSÃO REFATORADA

from django.urls import path

# Import específico de cada função para evitar conflitos
from .views.dashboard import (
    home, dashboard, configuracoes, parametro_list,
    parametro_create, parametro_update, relatorios,
    relatorio_clientes, relatorio_campanhas, relatorio_performance
)
from .views import usuario, cliente
# IMPORT DIRETO DA CLASSE WIZARD REFATORADA
from .views.cliente_wizard import ClienteWizardView

app_name = 'gestor'

urlpatterns = [
    # ===== PÁGINAS PRINCIPAIS =====
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    # ===== CLIENTE DE MARKETING - ESTRUTURA SIMPLIFICADA =====
    path('clientes/', cliente.cliente_list, name='cliente_list'),
    
    # CADASTRO RÁPIDO (Form Simples)
    path('clientes/novo/', cliente.cliente_create, name='cliente_create'),
    path('clientes/<uuid:pk>/editar/', cliente.cliente_update, name='cliente_update'),
    
    # BRIEFING ESTRATÉGICO (Wizard 4 Steps)
    path('clientes/<uuid:pk>/briefing/',
         ClienteWizardView.as_view(),
         name='cliente_briefing'),
    
    # VISUALIZAÇÃO E EXCLUSÃO
    path('clientes/<uuid:pk>/', cliente.cliente_detail, name='cliente_detail'),
    path('clientes/<uuid:pk>/excluir/', cliente.cliente_delete, name='cliente_delete'),
    
    # CHECKLIST OPERACIONAL
    path('clientes/<uuid:pk>/checklist/', cliente.cliente_checklist, name='cliente_checklist'),
    path('clientes/<uuid:pk>/checklist/editar/', cliente.cliente_checklist_update, name='cliente_checklist_update'),

    # ===== CAMPANHAS - SIMPLIFICADAS =====
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

    # ===== RELATÓRIOS =====
    path('relatorios/', relatorios, name='relatorios'),
    path('relatorios/clientes/', relatorio_clientes, name='relatorio_clientes'),
    path('relatorios/campanhas/', relatorio_campanhas, name='relatorio_campanhas'),
    path('relatorios/performance/', relatorio_performance, name='relatorio_performance'),
]