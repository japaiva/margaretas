# gestor/views/cliente.py - VIEWS DE CLIENTE

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from core.models import Cliente, ClienteChecklist, Campanha, ProdutoServicoEvento
from core.forms import ClienteForm, ClienteChecklistForm

import logging
logger = logging.getLogger(__name__)


# ===== VIEWS PRINCIPAIS DE CLIENTE =====

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
    """Detalhes do cliente com produtos/serviços e campanhas integrados"""
    
    # QUERY ÚNICA OTIMIZADA - Buscar cliente com todos os relacionamentos
    cliente = get_object_or_404(
        Cliente.objects.select_related().prefetch_related(
            # Prefetch otimizado para produtos/serviços
            Prefetch(
                'produtos_servicos',
                queryset=ProdutoServicoEvento.objects.order_by('-created_at')
            ),
            # Prefetch para campanhas
            'campanhas'
        ),
        pk=pk
    )
    
    # Produtos/Serviços com paginação inline
    produtos_servicos_qs = cliente.produtos_servicos.all()
    
    # Filtros para produtos/serviços (se aplicados)
    tipo_filter = request.GET.get('tipo_ps')
    status_filter = request.GET.get('status_ps')
    search_filter = request.GET.get('search_ps')
    
    if tipo_filter:
        produtos_servicos_qs = produtos_servicos_qs.filter(tipo=tipo_filter)
    
    if status_filter == 'ativo':
        produtos_servicos_qs = produtos_servicos_qs.filter(ativo=True)
    elif status_filter == 'inativo':
        produtos_servicos_qs = produtos_servicos_qs.filter(ativo=False)
    
    if search_filter:
        produtos_servicos_qs = produtos_servicos_qs.filter(
            Q(nome__icontains=search_filter) |
            Q(descricao__icontains=search_filter) |
            Q(caracteristicas_beneficios__icontains=search_filter)
        )
    
    # Paginação para produtos/serviços
    paginator_ps = Paginator(produtos_servicos_qs, 10)
    page_ps = request.GET.get('page_ps')
    produtos_servicos = paginator_ps.get_page(page_ps)
    
    # Campanhas recentes (primeiras 5)
    campanhas = cliente.campanhas.order_by('-created_at')[:5]
    
    # Buscar ou criar checklist
    checklist, created = ClienteChecklist.objects.get_or_create(cliente=cliente)
    if created:
        logger.info(f'Checklist criado automaticamente para cliente {cliente.nome_empresa}')
    
    # Estatísticas calculadas em uma única query
    stats = {
        'produtos_servicos_total': cliente.produtos_servicos.count(),
        'produtos_servicos_ativos': cliente.produtos_servicos.filter(ativo=True).count(),
        'produtos_servicos_por_tipo': {
            'produto': cliente.produtos_servicos.filter(tipo='produto').count(),
            'servico': cliente.produtos_servicos.filter(tipo='servico').count(),
            'curso': cliente.produtos_servicos.filter(tipo='curso').count(),
            'evento': cliente.produtos_servicos.filter(tipo='evento').count(),
        },
        'campanhas_total': cliente.campanhas.count(),
        'campanhas_ativas': cliente.campanhas.filter(status='ativa').count(),
        'briefing_progress': cliente.briefing_progress,
        'checklist_progress': checklist.completude_percentual,
    }
    
    context = {
        'cliente': cliente,
        'produtos_servicos': produtos_servicos,
        'campanhas': campanhas,
        'stats': stats,
        'checklist': checklist,
        'title': f'{cliente.nome_empresa}',
        
        # Filtros para produtos/serviços
        'tipo_filter': tipo_filter,
        'status_filter': status_filter,
        'search_filter': search_filter,
        
        # Choices para filtros
        'tipo_choices': ProdutoServicoEvento.TIPO_CHOICES,
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

            messages.success(request, f'✅ Cliente "{cliente.nome_empresa}" criado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} criado por {request.user.username}')

            action = request.POST.get('action')
            logger.debug('cliente_create: Ação do botão: %s', action)

            if action == 'save_and_wizard':
                logger.debug('cliente_create: Redirecionando para wizard.')
                return redirect('gestor:cliente_briefing', pk=cliente.pk)
            elif action == 'save_and_checklist':
                logger.debug('cliente_create: Redirecionando para checklist.')
                return redirect('gestor:cliente_checklist', pk=cliente.pk)
            else:
                logger.debug('cliente_create: Redirecionando para detalhes do cliente.')
                return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            logger.warning('cliente_create: Formulário é INVÁLIDO. Erros: %s', form.errors.as_json())
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
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
            
            messages.success(request, f'✅ Cliente "{cliente.nome_empresa}" atualizado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} atualizado por {request.user.username}')
            logger.debug('cliente_update: Redirecionando para detalhes do cliente.')
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            logger.warning('cliente_update: Formulário é INVÁLIDO. Erros: %s', form.errors.as_json())
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
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
            f'❌ Não é possível excluir o cliente "{cliente.nome_empresa}" pois possui campanhas ativas. '
            f'Pause ou finalize as campanhas primeiro.'
        )
        return redirect('gestor:cliente_detail', pk=pk)
    
    # EXCLUSÃO REAL - não apenas desativação
    nome_empresa = cliente.nome_empresa
    
    # Verificar dependências
    total_campanhas = cliente.campanhas.count()
    total_produtos_servicos = cliente.produtos_servicos.count()
    
    try:
        # Excluir cliente e todas as relações CASCADE
        cliente.delete()
        
        # Mensagem com dependências
        dependencias_msg = ""
        if total_campanhas > 0 or total_produtos_servicos > 0:
            dependencias = []
            if total_campanhas > 0:
                dependencias.append(f"{total_campanhas} campanha(s)")
            if total_produtos_servicos > 0:
                dependencias.append(f"{total_produtos_servicos} produto(s)/serviço(s)")
            dependencias_msg = f" ({', '.join(dependencias)} também foram removidos)"
        
        messages.success(
            request, 
            f'✅ Cliente "{nome_empresa}" excluído permanentemente com sucesso!{dependencias_msg}'
        )
        
        logger.info(f'Cliente {nome_empresa} excluído permanentemente por {request.user.username}')
        
    except Exception as e:
        logger.error(f'Erro ao excluir cliente {nome_empresa}: {e}')
        messages.error(
            request, 
            f'❌ Erro ao excluir cliente "{nome_empresa}". Tente novamente ou contate o suporte.'
        )
        return redirect('gestor:cliente_detail', pk=pk)
    
    return redirect('gestor:cliente_list')


# ===== VIEWS DE CHECKLIST =====
# Correção na view cliente_checklist
# No arquivo gestor/views/cliente.py

@login_required
def cliente_checklist(request, pk):
    """View para checklist - redireciona para detalhe do cliente"""
    
    # Como não temos template de detalhe do checklist,
    # redireciona direto para o detalhe do cliente
    print(f"🔍 DEBUG: cliente_checklist chamado - redirecionando para cliente_detail")
    
    # Garantir que o checklist existe
    cliente = get_object_or_404(Cliente, pk=pk)
    checklist, created = ClienteChecklist.objects.get_or_create(
        cliente=cliente,
        defaults={'updated_by': request.user}
    )
    
    if created:
        messages.info(request, f'📋 Checklist criado para {cliente.nome_empresa}')
    
    # Redirecionar sempre para o detalhe do cliente
    return redirect('gestor:cliente_detail', pk=pk)


@login_required
def cliente_checklist_update(request, pk):
    """View para editar checklist operacional de um cliente"""
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


# ===== WIZARD PARA BRIEFING DETALHADO =====

@login_required 
def cliente_briefing(request, pk):
    """Wrapper para o wizard de briefing estratégico"""
    # Redireciona para a view wizard separada
    from .cliente_wizard import ClienteWizardView
    
    cliente = get_object_or_404(Cliente, pk=pk)
    wizard_view = ClienteWizardView.as_view()
    return wizard_view(request, pk=pk)


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
        'produtos_servicos': {
            'total': cliente.produtos_servicos.count(),
            'ativos': cliente.produtos_servicos.filter(ativo=True).count(),
            'por_tipo': {
                'produto': cliente.produtos_servicos.filter(tipo='produto').count(),
                'servico': cliente.produtos_servicos.filter(tipo='servico').count(),
                'curso': cliente.produtos_servicos.filter(tipo='curso').count(),
                'evento': cliente.produtos_servicos.filter(tipo='evento').count(),
            }
        },
        'created_at': cliente.created_at.isoformat(),
        'updated_at': cliente.updated_at.isoformat(),
    }
    
    return JsonResponse(stats)