# gestor/views/cliente.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView


# ===== IMPORTS ATUALIZADOS =====
from core.models import Cliente, ClienteChecklist, Campanha
from core.forms import ClienteForm, CampanhaForm, ClienteChecklistForm

from core.forms.wizard_forms import (
    ClienteWizardStep1Form, 
    ClienteWizardStep2Form, 
    ClienteWizardStep3Form,
    ClienteWizardStep4Form,
    ClienteWizardConfirmForm
)

import logging
logger = logging.getLogger(__name__)





@login_required
def cliente_checklist(request, pk):
    """
    View para visualizar checklist operacional de um cliente
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Buscar ou criar checklist
    checklist, created = ClienteChecklist.objects.get_or_create(
        cliente=cliente,
        defaults={'updated_by': request.user}
    )
    
    context = {
        'cliente': cliente,
        'checklist': checklist,
        'is_new': created,
        'completude': checklist.completude_percentual,
        'page_title': f'Checklist Operacional - {cliente.nome_empresa}',
        'breadcrumbs': [
            {'url': 'gestor:cliente_list', 'title': 'Clientes'},
            {'url': 'gestor:cliente_detail', 'title': cliente.nome_empresa, 'args': [cliente.pk]},
            {'title': 'Checklist'},
        ]
    }
    
    return render(request, 'gestor/cliente/checklist_detail.html', context)

@login_required
def cliente_checklist_update(request, pk):
    """
    View para editar checklist operacional de um cliente
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Buscar ou criar checklist
    checklist, created = ClienteChecklist.objects.get_or_create(
        cliente=cliente,
        defaults={'updated_by': request.user}
    )
    
    if request.method == 'POST':
        form = ClienteChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.updated_by = request.user
            checklist.save()
            
            messages.success(
                request, 
                f'✅ Checklist do cliente {cliente.nome_empresa} atualizado com sucesso!'
            )
            return redirect('gestor:cliente_checklist', pk=cliente.pk)
        else:
            messages.error(request, '❌ Erro ao salvar checklist. Verifique os campos.')
    else:
        form = ClienteChecklistForm(instance=checklist)
    
    # Calcular progresso por seção se o método existir
    progress_data = {}
    if hasattr(form, 'field_sections'):
        for section_name in form.field_sections.keys():
            if hasattr(form, 'get_section_progress'):
                progress_data[section_name] = form.get_section_progress(section_name)
    
    context = {
        'cliente': cliente,
        'checklist': checklist,
        'form': form,
        'is_edit': True,
        'is_new': created,
        'progress_data': progress_data,
        'page_title': f'Editar Checklist - {cliente.nome_empresa}',
        'breadcrumbs': [
            {'url': 'gestor:cliente_list', 'title': 'Clientes'},
            {'url': 'gestor:cliente_detail', 'title': cliente.nome_empresa, 'args': [cliente.pk]},
            {'url': 'gestor:cliente_checklist', 'title': 'Checklist', 'args': [cliente.pk]},
            {'title': 'Editar'},
        ]
    }
    
    return render(request, 'gestor/cliente/checklist_form.html', context)



# ===== VIEWS DE CLIENTE =====

@login_required
def cliente_list(request):
    """Lista todos os clientes de marketing"""
    
    # Busca
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    briefing_filter = request.GET.get('briefing', '')
    
    # Query base
    clientes = Cliente.objects.select_related().order_by('-created_at')
    
    # Aplicar filtros
    if search:
        clientes = clientes.filter(
            Q(nome_empresa__icontains=search) |
            Q(responsavel_contrato__icontains=search) |
            Q(cnpj_cpf__icontains=search)
        )
    
    if status_filter:
        clientes = clientes.filter(ativo=(status_filter == 'ativo'))
    
    if briefing_filter:
        if briefing_filter == 'completo':
            clientes = clientes.filter(briefing_completo=True)
        elif briefing_filter == 'incompleto':
            clientes = clientes.filter(briefing_completo=False)
    
    # Paginação
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': Cliente.objects.count(),
        'ativos': Cliente.objects.filter(ativo=True).count(),
        'inativos': Cliente.objects.filter(ativo=False).count(),
        'briefing_completo': Cliente.objects.filter(briefing_completo=True).count(),
        'briefing_incompleto': Cliente.objects.filter(briefing_completo=False).count(),
        'com_campanhas': Cliente.objects.annotate(
            num_campanhas=Count('campanhas')
        ).filter(num_campanhas__gt=0).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'clientes': page_obj,
        'search': search,
        'status_filter': status_filter,
        'briefing_filter': briefing_filter,
        'stats': stats,
        'title': 'Clientes de Marketing'
    }
    
    return render(request, 'gestor/cliente/list.html', context)


@login_required
def cliente_detail(request, pk):
    """Detalhes de um cliente específico"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Buscar campanhas relacionadas
    campanhas = cliente.campanhas.order_by('-created_at')[:10]  # Últimas 10
    
    # Buscar ou criar checklist
    checklist, created = ClienteChecklist.objects.get_or_create(cliente=cliente)
    if created:
        logger.info(f'Checklist criado automaticamente para cliente {cliente.nome_empresa}')
    
    # Estatísticas do cliente
    stats = {
        'campanhas_total': cliente.campanhas.count(),
        'campanhas_ativas': cliente.campanhas.filter(status='ativa').count(),
        'campanhas_planejamento': cliente.campanhas.filter(status='planejamento').count(),
        'campanhas_finalizadas': cliente.campanhas.filter(status='finalizada').count(),
        'briefing_progress': cliente.briefing_progress,
        'checklist_progress': checklist.completude_percentual,
    }
    
    context = {
        'cliente': cliente,
        'campanhas': campanhas,
        'checklist': checklist,
        'stats': stats,
        'title': f'Cliente: {cliente.nome_empresa}'
    }
    
    return render(request, 'gestor/cliente/detail.html', context)

@login_required
def cliente_create(request):
    """Criar novo cliente"""
    
    logger.debug('cliente_create: Requisição recebida. Método: %s', request.method)
    cliente = None

    if request.method == 'POST':
        logger.debug('cliente_create: Método POST. Tentando processar formulário.')
        form = ClienteForm(request.POST, request.FILES)
        
        if form.is_valid():
            logger.debug('cliente_create: Formulário é VÁLIDO. Salvando cliente...')
            cliente = form.save(commit=False)
            cliente.created_by = request.user
            cliente.save()

            # Criar checklist automaticamente
            ClienteChecklist.objects.create(cliente=cliente)

            messages.success(request, f'Cliente "{cliente.nome_empresa}" criado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} criado por {request.user.username}')

            action = request.POST.get('action')
            logger.debug('cliente_create: Ação do botão: %s', action)

            if action == 'save_and_wizard':
                logger.debug('cliente_create: Redirecionando para wizard.')
                return redirect('gestor:cliente_wizard', pk=cliente.pk)
            elif action == 'save_and_checklist':
                logger.debug('cliente_create: Redirecionando para checklist.')
                return redirect('gestor:cliente_checklist', pk=cliente.pk)
            else:
                logger.debug('cliente_create: Redirecionando para detalhes do cliente.')
                return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            logger.warning('cliente_create: Formulário é INVÁLIDO. Erros: %s', form.errors.as_json())
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        logger.debug('cliente_create: Método GET. Renderizando formulário vazio.')
        form = ClienteForm()

    context = {
        'form': form,
        'cliente': cliente,
        'title': 'Novo Cliente',
        'subtitle': 'Cadastro de Cliente de Marketing',
        'action': 'Criar'
    }
    logger.debug('cliente_create: Renderizando gestor/cliente/form.html com contexto.')
    return render(request, 'gestor/cliente/form.html', context)

@login_required
def cliente_update(request, pk):
    """Editar cliente existente"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    logger.debug('cliente_update: Requisição recebida. Método: %s. Cliente PK: %s', request.method, pk)
    
    if request.method == 'POST':
        logger.debug('cliente_update: Método POST. Tentando processar formulário.')
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            logger.debug('cliente_update: Formulário é VÁLIDO. Atualizando cliente...')
            cliente = form.save()
            
            messages.success(request, f'Cliente "{cliente.nome_empresa}" atualizado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} atualizado por {request.user.username}')
            logger.debug('cliente_update: Redirecionando para detalhes do cliente.')
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            logger.warning('cliente_update: Formulário é INVÁLIDO. Erros: %s', form.errors.as_json())
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        logger.debug('cliente_update: Método GET. Renderizando formulário existente.')
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Editar: {cliente.nome_empresa}',
        'subtitle': 'Edição de Cliente',
        'action': 'Atualizar'
    }
    logger.debug('cliente_update: Renderizando gestor/cliente/form.html com contexto.')
    return render(request, 'gestor/cliente/form.html', context)

@login_required
@require_http_methods(["POST"])
def cliente_delete(request, pk):
    """Excluir cliente completamente (exclusão real)"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Verificar se tem campanhas ativas
    campanhas_ativas = cliente.campanhas.filter(status__in=['ativa', 'aprovacao'])
    
    if campanhas_ativas.exists():
        messages.error(
            request, 
            f'Não é possível excluir o cliente "{cliente.nome_empresa}" pois possui campanhas ativas. '
            f'Pause ou finalize as campanhas primeiro.'
        )
        return redirect('gestor:cliente_detail', pk=pk)
    
    # EXCLUSÃO REAL - não apenas desativação
    nome_empresa = cliente.nome_empresa
    
    # Opcional: Verificar se tem dependências importantes
    total_campanhas = cliente.campanhas.count()
    
    try:
        # Excluir cliente e todas as relações CASCADE
        cliente.delete()
        
        messages.success(
            request, 
            f'Cliente "{nome_empresa}" excluído permanentemente com sucesso! '
            f'{"" if total_campanhas == 0 else f"({total_campanhas} campanhas também foram removidas)"}'
        )
        
        logger.info(f'Cliente {nome_empresa} excluído permanentemente por {request.user.username}')
        
    except Exception as e:
        logger.error(f'Erro ao excluir cliente {nome_empresa}: {e}')
        messages.error(
            request, 
            f'Erro ao excluir cliente "{nome_empresa}". Tente novamente ou contate o suporte.'
        )
        return redirect('gestor:cliente_detail', pk=pk)
    
    return redirect('gestor:cliente_list')



# ===== VIEWS DE CHECKLIST =====

@login_required
def cliente_checklist(request, pk):
    """Gerenciar checklist operacional do cliente"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    checklist, created = ClienteChecklist.objects.get_or_create(cliente=cliente)
    
    if request.method == 'POST':
        form = ClienteChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            checklist = form.save(commit=False)
            checklist.updated_by = request.user
            checklist.save()
            
            messages.success(request, 'Checklist operacional atualizado com sucesso!')
            logger.info(f'Checklist do cliente {cliente.nome_empresa} atualizado por {request.user.username}')
            
            # Redirecionar baseado na ação
            action = request.POST.get('action', 'stay')
            if action == 'save_and_return':
                return redirect('gestor:cliente_detail', pk=cliente.pk)
            # Senão, permanece na mesma página para continuar editando
            
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ClienteChecklistForm(instance=checklist)
    
    context = {
        'form': form,
        'cliente': cliente,
        'checklist': checklist,
        'title': f'Checklist Operacional - {cliente.nome_empresa}',
        'progress': checklist.completude_percentual,
    }
    
    return render(request, 'gestor/cliente/checklist.html', context)


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
            
            messages.success(request, f'Campanha "{campanha.nome_campanha}" criada com sucesso!')
            
            return redirect('gestor:campanha_detail', pk=campanha.pk)
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
            
            messages.success(request, f'Campanha "{campanha.nome_campanha}" atualizada com sucesso!')
            
            return redirect('gestor:campanha_detail', pk=campanha.pk)
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
        messages.error(request, 'Não é possível excluir uma campanha ativa. Pause ou finalize primeiro.')
        return redirect('gestor:campanha_detail', pk=pk)
    
    nome = campanha.nome_campanha
    cliente_id = campanha.cliente.pk
    campanha.delete()
    
    messages.success(request, f'Campanha "{nome}" excluída com sucesso!')
    
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
            f'Status da campanha "{campanha.nome_campanha}" alterado de {old_status} para {campanha.get_status_display()}'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Status alterado com sucesso',
            'new_status': campanha.get_status_display()
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Status inválido'
    })


# ===== VIEWS DE API =====

@login_required
def cliente_api_search(request):
    """API para busca de clientes (para autocomplete)"""
    
    term = request.GET.get('term', '')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    clientes = Cliente.objects.filter(
        Q(nome_empresa__icontains=term) |
        Q(responsavel_contrato__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for cliente in clientes:
        results.append({
            'id': str(cliente.pk),  # UUID precisa ser string
            'text': cliente.nome_empresa,
            'responsavel': cliente.responsavel_contrato or '',
            'briefing_completo': cliente.briefing_completo,
            'briefing_progress': cliente.briefing_progress
        })
    
    return JsonResponse({'results': results})


@login_required
def cliente_api_stats(request, pk):
    """API para estatísticas de um cliente"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    checklist, _ = ClienteChecklist.objects.get_or_create(cliente=cliente)
    
    stats = {
        'nome_empresa': cliente.nome_empresa,
        'ativo': cliente.ativo,
        'briefing_completo': cliente.briefing_completo,
        'briefing_progress': cliente.briefing_progress,
        'checklist_progress': checklist.completude_percentual,
        'campanhas': {
            'total': cliente.campanhas.count(),
            'ativas': cliente.campanhas.filter(status='ativa').count(),
            'planejamento': cliente.campanhas.filter(status='planejamento').count(),
            'finalizadas': cliente.campanhas.filter(status='finalizada').count(),
        },
        'created_at': cliente.created_at.isoformat(),
        'updated_at': cliente.updated_at.isoformat(),
    }
    
    return JsonResponse(stats)


# ===== WIZARD PARA BRIEFING DETALHADO =====
# Nota: A implementação completa do wizard está em gestor/views/cliente_wizard.py

@login_required 
def cliente_wizard(request, pk):
    """Wrapper para o wizard de briefing estratégico"""
    # Redireciona para a view wizard separada
    from .cliente_wizard import ClienteWizardView
    
    cliente = get_object_or_404(Cliente, pk=pk)
    wizard_view = ClienteWizardView.as_view()
    return wizard_view(request, pk=pk)
