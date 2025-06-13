# gestor/views/cliente.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from core.models import Cliente, ProdutoServicoEvento, Campanha
from core.forms import ClienteForm, ProdutoServicoEventoForm, CampanhaForm

import logging
logger = logging.getLogger(__name__)


# ===== VIEWS DE CLIENTE =====

@login_required
def cliente_list(request):
    """Lista todos os clientes de marketing"""
    
    # Busca
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Query base
    clientes = Cliente.objects.select_related().order_by('-created_at')
    
    # Aplicar filtros
    if search:
        clientes = clientes.filter(
            Q(nome_empresa__icontains=search) |
            Q(responsavel_contrato__icontains=search)
        )
    
    if status_filter:
        clientes = clientes.filter(ativo=(status_filter == 'ativo'))
    
    # Paginação
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': Cliente.objects.count(),
        'ativos': Cliente.objects.filter(ativo=True).count(),
        'inativos': Cliente.objects.filter(ativo=False).count(),
        'com_campanhas': Cliente.objects.annotate(
            num_campanhas=Count('campanhas')
        ).filter(num_campanhas__gt=0).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'clientes': page_obj,
        'search': search,
        'status_filter': status_filter,
        'stats': stats,
        'title': 'Clientes de Marketing'
    }
    
    return render(request, 'gestor/cliente/list.html', context)


@login_required
def cliente_detail(request, pk):
    """Detalhes de um cliente específico"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Buscar produtos/serviços relacionados - CORRIGIDO
    produtos_servicos = cliente.produtos_servicos_relacionados.filter(ativo=True).order_by('-created_at')
    
    # Buscar campanhas relacionadas
    campanhas = cliente.campanhas.order_by('-created_at')[:10]  # Últimas 10
    
    # Estatísticas do cliente
    stats = {
        'produtos_servicos': produtos_servicos.count(),
        'campanhas_total': cliente.campanhas.count(),
        'campanhas_ativas': cliente.campanhas.filter(status='ativa').count(),
        'campanhas_finalizadas': cliente.campanhas.filter(status='finalizada').count(),
    }
    
    context = {
        'cliente': cliente,
        'produtos_servicos': produtos_servicos,
        'campanhas': campanhas,
        'stats': stats,
        'title': f'Cliente: {cliente.nome_empresa}'
    }
    
    return render(request, 'gestor/cliente/detail.html', context)

@login_required
def cliente_create(request):
    """Criar novo cliente"""
    
    cliente = None  # valor default, usado no render inicial (GET)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.created_by = request.user
            cliente.save()

            messages.success(request, f'Cliente "{cliente.nome_empresa}" criado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} criado por {request.user.username}')

            if request.POST.get('action') == 'save_and_wizard':
                return redirect('cliente_wizard_step1', pk=cliente.pk)
            else:
                return redirect('gestor:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm()

    context = {
        'form': form,
        'cliente': cliente,
        'title': 'Novo Cliente',
        'subtitle': 'Cadastro de Cliente de Marketing',
        'action': 'Criar'
    }

    return render(request, 'gestor/cliente/form.html', context)

@login_required
def cliente_update(request, pk):
    """Editar cliente existente"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            
            messages.success(request, f'Cliente "{cliente.nome_empresa}" atualizado com sucesso!')
            logger.info(f'Cliente {cliente.nome_empresa} atualizado por {request.user.username}')
            
            return redirect('gestor:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Editar: {cliente.nome_empresa}',
        'subtitle': 'Edição de Cliente',
        'action': 'Atualizar'
    }
    
    return render(request, 'gestor/cliente/form.html', context)


@login_required
@require_http_methods(["POST"])
def cliente_delete(request, pk):
    """Excluir cliente (soft delete)"""
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Verificar se tem campanhas ativas
    campanhas_ativas = cliente.campanhas.filter(status__in=['ativa', 'aprovacao'])
    
    if campanhas_ativas.exists():
        messages.error(
            request, 
            f'Não é possível excluir o cliente "{cliente.nome_empresa}" pois possui campanhas ativas.'
        )
        return redirect('gestor:cliente_detail', pk=pk)
    
    # Soft delete
    nome_empresa = cliente.nome_empresa
    cliente.ativo = False
    cliente.save()
    
    messages.success(request, f'Cliente "{nome_empresa}" desativado com sucesso!')
    logger.info(f'Cliente {nome_empresa} desativado por {request.user.username}')
    
    return redirect('gestor:cliente_list')


# ===== VIEWS DE PRODUTO/SERVIÇO/EVENTO =====

@login_required
def produto_servico_list(request, cliente_id):
    """Lista produtos/serviços de um cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    # Filtros
    tipo_filter = request.GET.get('tipo', '')
    search = request.GET.get('search', '')
    
    # Query - CORRIGIDO
    produtos = cliente.produtos_servicos_relacionados.filter(ativo=True).order_by('-created_at')
    
    if tipo_filter:
        produtos = produtos.filter(tipo=tipo_filter)
    
    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) |
            Q(descricao__icontains=search)
        )
    
    # Estatísticas por tipo
    stats = {
        'total': produtos.count(),
        'produtos': produtos.filter(tipo='produto').count(),
        'servicos': produtos.filter(tipo='servico').count(),
        'cursos': produtos.filter(tipo='curso').count(),
        'eventos': produtos.filter(tipo='evento').count(),
    }
    
    context = {
        'cliente': cliente,
        'produtos': produtos,
        'tipo_filter': tipo_filter,
        'search': search,
        'stats': stats,
        'title': f'Produtos/Serviços - {cliente.nome_empresa}'
    }
    
    return render(request, 'gestor/produto_servico/list.html', context)


@login_required
def produto_servico_create(request, cliente_id):
    """Criar novo produto/serviço para cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == 'POST':
        form = ProdutoServicoEventoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.cliente = cliente
            produto.save()
            
            messages.success(request, f'{produto.get_tipo_display()} "{produto.nome}" criado com sucesso!')
            
            return redirect('gestor:produto_servico_detail', pk=produto.pk)
    else:
        form = ProdutoServicoEventoForm()
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Novo Produto/Serviço - {cliente.nome_empresa}',
        'action': 'Criar'
    }
    
    return render(request, 'gestor/produto_servico/form.html', context)


@login_required
def produto_servico_detail(request, pk):
    """Detalhes de produto/serviço"""
    
    produto = get_object_or_404(ProdutoServicoEvento, pk=pk)
    
    # Campanhas relacionadas
    campanhas = produto.campanhas.order_by('-created_at')
    
    context = {
        'produto': produto,
        'cliente': produto.cliente,
        'campanhas': campanhas,
        'title': f'{produto.get_tipo_display()}: {produto.nome}'
    }
    
    return render(request, 'gestor/produto_servico/detail.html', context)


@login_required
def produto_servico_update(request, pk):
    """Editar produto/serviço"""
    
    produto = get_object_or_404(ProdutoServicoEvento, pk=pk)
    
    if request.method == 'POST':
        form = ProdutoServicoEventoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            
            messages.success(request, f'{produto.get_tipo_display()} "{produto.nome}" atualizado com sucesso!')
            
            return redirect('gestor:produto_servico_detail', pk=produto.pk)
    else:
        form = ProdutoServicoEventoForm(instance=produto)
    
    context = {
        'form': form,
        'produto': produto,
        'cliente': produto.cliente,
        'title': f'Editar: {produto.nome}',
        'action': 'Atualizar'
    }
    
    return render(request, 'gestor/produto_servico/form.html', context)


@login_required
@require_http_methods(["POST"])
def produto_servico_delete(request, pk):
    """Excluir produto/serviço"""
    
    produto = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente_id = produto.cliente.pk
    
    # Verificar campanhas ativas
    campanhas_ativas = produto.campanhas.filter(status__in=['ativa', 'aprovacao'])
    
    if campanhas_ativas.exists():
        messages.error(
            request,
            f'Não é possível excluir "{produto.nome}" pois possui campanhas ativas.'
        )
        return redirect('gestor:produto_servico_detail', pk=pk)
    
    nome = produto.nome
    produto.ativo = False
    produto.save()
    
    messages.success(request, f'"{nome}" desativado com sucesso!')
    
    return redirect('gestor:produto_servico_list', cliente_id=cliente_id)


# ===== VIEWS DE CAMPANHA =====

@login_required
def campanha_list(request):
    """Lista todas as campanhas"""
    
    # Filtros
    status_filter = request.GET.get('status', '')
    cliente_filter = request.GET.get('cliente', '')
    search = request.GET.get('search', '')
    
    # Query
    campanhas = Campanha.objects.select_related('cliente', 'produto_servico').order_by('-created_at')
    
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
        'produto_servico': campanha.produto_servico,
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
    campanha.delete()
    
    messages.success(request, f'Campanha "{nome}" excluída com sucesso!')
    
    return redirect('gestor:campanha_list')


# ===== VIEWS DE API =====

@login_required
def cliente_api_search(request):
    """API para busca de clientes (para autocomplete)"""
    
    term = request.GET.get('term', '')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    clientes = Cliente.objects.filter(
        Q(nome_empresa__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for cliente in clientes:
        results.append({
            'id': cliente.pk,
            'text': cliente.nome_empresa,
            'responsavel': cliente.responsavel_contrato or ''
        })
    
    return JsonResponse({'results': results})


@login_required
def produto_servico_api_by_cliente(request, cliente_id):
    """API para buscar produtos/serviços de um cliente"""
    
    produtos = ProdutoServicoEvento.objects.filter(
        cliente_id=cliente_id,
        ativo=True
    ).order_by('nome')
    
    results = []
    for produto in produtos:
        results.append({
            'id': produto.pk,
            'nome': produto.nome,
            'tipo': produto.get_tipo_display(),
            'preco': float(produto.preco) if produto.preco else None
        })
    
    return JsonResponse({'results': results})

# ===== FUNÇÕES WIZARD FALTANDO =====

@login_required
def cliente_wizard_step1(request, pk):
    """Wizard Step 1 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)


@login_required
def cliente_wizard_step2(request, pk):
    """Wizard Step 2 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)

@login_required
def cliente_wizard_step3(request, pk):
    """Wizard Step 3 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)

@login_required
def cliente_wizard_step4(request, pk):
    """Wizard Step 4 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)

@login_required
def cliente_wizard_step5(request, pk):
    """Wizard Step 5 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)

@login_required
def cliente_wizard_step6(request, pk):
    """Wizard Step 6 - Placeholder"""
    cliente = get_object_or_404(Cliente, pk=pk)
    return redirect('gestor:cliente_detail', pk=pk)

# ===== FUNÇÕES HTMX FALTANDO =====

@login_required
def cliente_form_htmx(request):
    """Form HTMX para cliente - Placeholder"""
    return JsonResponse({'status': 'ok'})

@login_required
def campanha_form_htmx(request):
    """Form HTMX para campanha - Placeholder"""
    return JsonResponse({'status': 'ok'})