# gestor/urls.py - ROTAS CORRIGIDAS PARA WIZARD

from django.urls import path
from . import views
from .views.cliente_wizard import ClienteWizardView  # ✅ IMPORTAR O WIZARD

app_name = 'gestor'

urlpatterns = [
    # ===== DASHBOARD =====
    path('', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),
    
    # ===== CLIENTES =====
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<uuid:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<uuid:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('clientes/<uuid:pk>/excluir/', views.cliente_delete, name='cliente_delete'),
    
    # ===== BRIEFING E CHECKLIST =====
    # ✅ CORREÇÃO: Usar diretamente o ClienteWizardView
    path('clientes/<uuid:pk>/briefing/', 
         ClienteWizardView.as_view(), 
         name='cliente_briefing'),
    path('clientes/<uuid:pk>/checklist/', views.cliente_checklist, name='cliente_checklist'),
    path('clientes/<uuid:pk>/checklist/editar/', views.cliente_checklist_update, name='cliente_checklist_update'),
    
    # ===== PRODUTOS/SERVIÇOS INLINE (SEM DETALHES) =====
    path('clientes/<uuid:cliente_pk>/produto-servico/novo/', 
         views.produto_servico_create_inline, 
         name='produto_servico_create_inline'),
         
    path('produto-servico/<uuid:pk>/editar-inline/', 
         views.produto_servico_update_inline, 
         name='produto_servico_update_inline'),
         
    path('produto-servico/<uuid:pk>/excluir-inline/', 
         views.produto_servico_delete_inline, 
         name='produto_servico_delete_inline'),
         
    path('produto-servico/<uuid:pk>/toggle-status-inline/', 
         views.produto_servico_toggle_status_inline, 
         name='produto_servico_toggle_status_inline'),
    
    # ===== CAMPANHAS =====
    path('campanhas/', views.campanha_list, name='campanha_list'),
    path('campanhas/nova/', views.campanha_create, name='campanha_create'),
    path('campanhas/<uuid:pk>/', views.campanha_detail, name='campanha_detail'),
    path('campanhas/<uuid:pk>/editar/', views.campanha_update, name='campanha_update'),
    path('campanhas/<uuid:pk>/excluir/', views.campanha_delete, name='campanha_delete'),
    path('campanhas/<uuid:pk>/status/', views.campanha_change_status, name='campanha_change_status'),
    
    # ===== API =====
    path('api/clientes/buscar/', views.cliente_api_search, name='cliente_api_search'),
    path('api/clientes/<uuid:pk>/stats/', views.cliente_api_stats, name='cliente_api_stats'),
    
    # ===== CONFIGURAÇÕES =====
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('parametros/', views.parametro_list, name='parametro_list'),
    path('parametros/novo/', views.parametro_create, name='parametro_create'),
    path('parametros/<int:pk>/editar/', views.parametro_update, name='parametro_update'),
    
    # ===== RELATÓRIOS =====
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/clientes/', views.relatorio_clientes, name='relatorio_clientes'),
    path('relatorios/campanhas/', views.relatorio_campanhas, name='relatorio_campanhas'),
    path('relatorios/performance/', views.relatorio_performance, name='relatorio_performance'),
]