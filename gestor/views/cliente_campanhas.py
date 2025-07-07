# gestor/views/cliente_campanhas.py - VIEWS DE CAMPANHAS

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django import forms

from core.models import Cliente, Campanha
from core.forms import CampanhaForm

import logging
logger = logging.getLogger(__name__)


# ===== VIEWS DE CAMPANHA =====

@login_required
def campanha_list(request):
    """Lista todas as campanhas"""
    
    # Filtros
    status_filter = request.GET.get('status', '')
    cliente_filter = request.GET.get('cliente', '')
    search = request.GET.get('search', '')
    
    # Query
    campanhas = Campanha.objects.select_related('cliente').order_by('-created_at')
    
    if status_filter:
        campanhas = campanhas.filter(status=status_filter)
    
    if cliente_filter:
        campanhas = campanhas.filter(cliente_id=cliente_filter)
    
    if search:
        campanhas = campanhas.filter(
            Q(nome_campanha__icontains=search) |
            Q(cliente__nome_empresa__icontains=search) |
            Q(objetivo_principal__icontains=search)
        )
    
    # Paginação
    paginator = Paginator(campanhas, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': Campanha.objects.count(),
        'ativas': Campanha.objects.filter(status='ativa').count(),
        'planejamento': Campanha.objects.filter(status='planejamento').count(),
        'finalizadas': Campanha.objects.filter(status='finalizada').count(),
        'pausadas': Campanha.objects.filter(status='pausada').count(),
    }
    
    # Lista de clientes para filtro
    clientes = Cliente.objects.filter(ativo=True).order_by('nome_empresa')
    
    context = {
        'page_obj': page_obj,
        'campanhas': page_obj,
        'stats': stats,
        'clientes': clientes,
        'status_filter': status_filter,
        'cliente_filter': cliente_filter,
        'search': search,
        'title': 'Campanhas de Marketing'
    }
    
    return render(request, 'gestor/campanha/list.html', context)


@login_required
def campanha_detail(request, pk):
    """Detalhes de uma campanha"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    
    context = {
        'campanha': campanha,
        'cliente': campanha.cliente,
        'title': f'Campanha: {campanha.nome_campanha}'
    }
    
    return render(request, 'gestor/campanha/detail.html', context)


@login_required
def campanha_create(request):
    """Criar nova campanha"""
    
    if request.method == 'POST':
        form = CampanhaForm(request.POST)
        if form.is_valid():
            campanha = form.save(commit=False)
            campanha.created_by = request.user
            campanha.save()
            
            messages.success(request, f'✅ Campanha "{campanha.nome_campanha}" criada com sucesso!')
            logger.info(f'Campanha {campanha.nome_campanha} criada por {request.user.username}')
            
            return redirect('gestor:campanha_detail', pk=campanha.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = CampanhaForm()
        
        # Pré-selecionar cliente se vier da URL
        cliente_id = request.GET.get('cliente_id')
        if cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id, ativo=True)
                form.fields['cliente'].initial = cliente
                form.fields['cliente'].widget.attrs['readonly'] = True
            except Cliente.DoesNotExist:
                pass
    
    context = {
        'form': form,
        'title': 'Nova Campanha',
        'subtitle': 'Criação de Campanha de Marketing',
        'action': 'Criar'
    }
    
    return render(request, 'gestor/campanha/form.html', context)


@login_required
def campanha_update(request, pk):
    """Editar campanha"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    
    if request.method == 'POST':
        form = CampanhaForm(request.POST, instance=campanha)
        if form.is_valid():
            campanha = form.save()
            
            messages.success(request, f'✅ Campanha "{campanha.nome_campanha}" atualizada com sucesso!')
            logger.info(f'Campanha {campanha.nome_campanha} atualizada por {request.user.username}')
            
            return redirect('gestor:campanha_detail', pk=campanha.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = CampanhaForm(instance=campanha)
    
    context = {
        'form': form,
        'campanha': campanha,
        'title': f'Editar: {campanha.nome_campanha}',
        'action': 'Atualizar'
    }
    
    return render(request, 'gestor/campanha/form.html', context)


@login_required
@require_http_methods(["POST"])
def campanha_delete(request, pk):
    """Excluir campanha"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    
    # Verificar se pode ser deletada
    if campanha.status == 'ativa':
        messages.error(request, '❌ Não é possível excluir uma campanha ativa. Pause ou finalize primeiro.')
        return redirect('gestor:campanha_detail', pk=pk)
    
    nome = campanha.nome_campanha
    cliente_nome = campanha.cliente.nome_empresa
    campanha.delete()
    
    messages.success(request, f'✅ Campanha "{nome}" excluída com sucesso!')
    logger.info(f'Campanha {nome} do cliente {cliente_nome} excluída por {request.user.username}')
    
    return redirect('gestor:campanha_list')


@login_required
@require_http_methods(["POST"])
def campanha_change_status(request, pk):
    """Alterar status da campanha via AJAX"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    new_status = request.POST.get('status')
    
    if new_status in dict(Campanha.STATUS_CHOICES):
        old_status = campanha.get_status_display()
        campanha.status = new_status
        campanha.save()
        
        messages.success(
            request, 
            f'✅ Status da campanha "{campanha.nome_campanha}" alterado de {old_status} para {campanha.get_status_display()}'
        )
        
        logger.info(f'Status da campanha {campanha.nome_campanha} alterado de {old_status} para {campanha.get_status_display()}')
        
        return JsonResponse({
            'success': True,
            'message': 'Status alterado com sucesso',
            'new_status': campanha.get_status_display()
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Status inválido'
    })


# ===== VIEWS INLINE PARA CAMPANHAS (se necessário) =====

@login_required
def campanha_create_inline(request, cliente_pk):
    """Criar campanha inline no contexto do cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    if request.method == 'POST':
        form = CampanhaForm(request.POST)
        if form.is_valid():
            campanha = form.save(commit=False)
            campanha.cliente = cliente
            campanha.created_by = request.user
            campanha.save()
            
            messages.success(
                request, 
                f'✅ Campanha "{campanha.nome_campanha}" criada com sucesso!'
            )
            logger.info(f'Campanha {campanha.nome_campanha} criada inline para cliente {cliente.nome_empresa}')
            
            # Retornar para o detalhe do cliente
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = CampanhaForm()
        # Pré-configurar o cliente
        form.fields['cliente'].initial = cliente
        form.fields['cliente'].widget = forms.HiddenInput()  # Esconder o campo cliente
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Nova Campanha - {cliente.nome_empresa}',
        'action': 'Criar',
        'is_inline': True,
        'cancel_url': reverse('gestor:cliente_detail', args=[cliente.pk]),
    }
    
    return render(request, 'gestor/campanha/form_inline.html', context)


@login_required
def campanha_update_inline(request, pk):
    """Editar campanha inline no contexto do cliente"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    cliente = campanha.cliente
    
    if request.method == 'POST':
        form = CampanhaForm(request.POST, instance=campanha)
        if form.is_valid():
            campanha = form.save()
            
            messages.success(
                request,
                f'✅ Campanha "{campanha.nome_campanha}" atualizada com sucesso!'
            )
            logger.info(f'Campanha {campanha.nome_campanha} atualizada inline')
            
            # Retornar para o detalhe do cliente
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = CampanhaForm(instance=campanha)
        form.fields['cliente'].widget = forms.HiddenInput()  # Esconder o campo cliente
    
    context = {
        'form': form,
        'campanha': campanha,
        'cliente': cliente,
        'title': f'Editar Campanha: {campanha.nome_campanha}',
        'action': 'Atualizar',
        'is_inline': True,
        'cancel_url': reverse('gestor:cliente_detail', args=[cliente.pk]),
    }
    
    return render(request, 'gestor/campanha/form_inline.html', context)


@login_required
@require_http_methods(["POST"])
def campanha_delete_inline(request, pk):
    """Excluir campanha inline no contexto do cliente"""
    
    campanha = get_object_or_404(Campanha, pk=pk)
    cliente = campanha.cliente
    
    # Verificar se pode ser deletada
    if campanha.status == 'ativa':
        messages.error(request, '❌ Não é possível excluir uma campanha ativa. Pause ou finalize primeiro.')
        return redirect('gestor:cliente_detail', pk=cliente.pk)
    
    nome = campanha.nome_campanha
    
    try:
        campanha.delete()
        
        messages.success(
            request,
            f'✅ Campanha "{nome}" excluída com sucesso!'
        )
        
        logger.info(f'Campanha {nome} excluída inline do cliente {cliente.nome_empresa}')
        
    except Exception as e:
        logger.error(f'Erro ao excluir campanha {nome}: {e}')
        messages.error(
            request,
            f'❌ Erro ao excluir campanha "{nome}". Tente novamente.'
        )
    
    return redirect('gestor:cliente_detail', pk=cliente.pk)


# ===== VIEWS DE API PARA CAMPANHAS =====

@login_required
def campanha_api_search(request):
    """API para busca de campanhas (para autocomplete)"""
    
    term = request.GET.get('term', '')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    campanhas = Campanha.objects.filter(
        Q(nome_campanha__icontains=term) |
        Q(objetivo_principal__icontains=term) |
        Q(cliente__nome_empresa__icontains=term)
    ).select_related('cliente')[:10]
    
    results = []
    for campanha in campanhas:
        results.append({
            'id': str(campanha.pk),
            'text': campanha.nome_campanha,
            'cliente': campanha.cliente.nome_empresa,
            'status': campanha.get_status_display(),
            'status_code': campanha.status,
            'orcamento': float(campanha.orcamento_total) if campanha.orcamento_total else None
        })
    
    return JsonResponse({'results': results})


@login_required
def cliente_campanhas_stats(request, cliente_pk):
    """API para estatísticas de campanhas de um cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    campanhas = cliente.campanhas.all()
    
    stats = {
        'total': campanhas.count(),
        'por_status': {},
        'orcamento_total': 0,
        'campanhas_recentes': []
    }
    
    # Estatísticas por status
    for status_code, status_nome in Campanha.STATUS_CHOICES:
        count = campanhas.filter(status=status_code).count()
        stats['por_status'][status_code] = {
            'nome': status_nome,
            'count': count
        }
    
    # Orçamento total
    campanhas_com_orcamento = campanhas.exclude(orcamento_total__isnull=True)
    if campanhas_com_orcamento.exists():
        stats['orcamento_total'] = sum(
            float(c.orcamento_total) for c in campanhas_com_orcamento
        )
    
    # Campanhas recentes
    campanhas_recentes = campanhas.order_by('-created_at')[:5]
    for campanha in campanhas_recentes:
        stats['campanhas_recentes'].append({
            'id': str(campanha.pk),
            'nome': campanha.nome_campanha,
            'status': campanha.get_status_display(),
            'created_at': campanha.created_at.isoformat()
        })
    
    return JsonResponse(stats)