# gestor/views/dashboard.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from core.models import Cliente,  Campanha
from core.models.base import Usuario

@login_required
def home(request):
    """
    Página inicial do Portal do Gestor
    """
    return render(request, 'gestor/home.html')

@login_required
def dashboard(request):
    """View para o dashboard do gestor"""
    context = {
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
        'total_campanhas': Campanha.objects.count(),
        'campanhas_ativas': Campanha.objects.filter(status='ativa').count(),
        'total_usuarios': Usuario.objects.filter(is_active=True).count(),
        
        # Estatísticas adicionais
        'clientes_com_campanhas': Cliente.objects.annotate(
            num_campanhas=Count('campanhas')
        ).filter(num_campanhas__gt=0).count(),
        
        'campanhas_por_status': {
            'planejamento': Campanha.objects.filter(status='planejamento').count(),
            'ativa': Campanha.objects.filter(status='ativa').count(),
            'pausada': Campanha.objects.filter(status='pausada').count(),
            'finalizada': Campanha.objects.filter(status='finalizada').count(),
        }
    }
    return render(request, 'gestor/dashboard.html', context)

@login_required
def configuracoes(request):
    """View para configurações do sistema"""
    return render(request, 'gestor/configuracoes.html')

@login_required
def parametro_list(request):
    """Lista de parâmetros do sistema"""
    from core.models.base import Parametro
    parametros = Parametro.objects.all().order_by('categoria', 'parametro')
    return render(request, 'gestor/parametro_list.html', {'parametros': parametros})

@login_required
def parametro_create(request):
    """Criar novo parâmetro"""
    return render(request, 'gestor/parametro_form.html')

@login_required
def parametro_update(request, pk):
    """Editar parâmetro"""
    return render(request, 'gestor/parametro_form.html')

@login_required
def relatorios(request):
    """Dashboard de relatórios"""
    return render(request, 'gestor/relatorios.html')

@login_required
def relatorio_clientes(request):
    """Relatório de clientes"""
    return render(request, 'gestor/relatorio_clientes.html')

@login_required
def relatorio_campanhas(request):
    """Relatório de campanhas"""
    return render(request, 'gestor/relatorio_campanhas.html')

@login_required
def relatorio_performance(request):
    """Relatório de performance"""
    return render(request, 'gestor/relatorio_performance.html')