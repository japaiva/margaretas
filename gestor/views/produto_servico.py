# gestor/views/produto_servico.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.models import Cliente
from core.models.produto_servico import ProdutoServicoEvento
from core.forms.produto_servico_forms import ProdutoServicoEventoForm, ProdutoServicoEventoFilterForm

import logging
logger = logging.getLogger(__name__)


@login_required
def produto_servico_list(request, cliente_pk):
    """Lista produtos/serviços de um cliente específico"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    # Filtros
    filter_form = ProdutoServicoEventoFilterForm(request.GET)
    produtos_servicos = cliente.produtos_servicos.order_by('-created_at')
    
    if filter_form.is_valid():
        # Aplicar filtros
        if filter_form.cleaned_data.get('tipo'):
            produtos_servicos = produtos_servicos.filter(tipo=filter_form.cleaned_data['tipo'])
        
        if filter_form.cleaned_data.get('status'):
            status = filter_form.cleaned_data['status']
            produtos_servicos = produtos_servicos.filter(ativo=(status == 'ativo'))
        
        if filter_form.cleaned_data.get('search'):
            search = filter_form.cleaned_data['search']
            produtos_servicos = produtos_servicos.filter(
                Q(nome__icontains=search) |
                Q(descricao__icontains=search) |
                Q(caracteristicas_beneficios__icontains=search)
            )
    
    # Paginação
    paginator = Paginator(produtos_servicos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    stats = {
        'total': cliente.produtos_servicos.count(),
        'ativos': cliente.produtos_servicos.filter(ativo=True).count(),
        'inativos': cliente.produtos_servicos.filter(ativo=False).count(),
        'por_tipo': {
            'produto': cliente.produtos_servicos.filter(tipo='produto').count(),
            'servico': cliente.produtos_servicos.filter(tipo='servico').count(),
            'curso': cliente.produtos_servicos.filter(tipo='curso').count(),
            'evento': cliente.produtos_servicos.filter(tipo='evento').count(),
        }
    }
    
    context = {
        'cliente': cliente,
        'page_obj': page_obj,
        'produtos_servicos': page_obj,
        'filter_form': filter_form,
        'stats': stats,
        'title': f'Produtos/Serviços - {cliente.nome_empresa}'
    }
    
    return render(request, 'gestor/produto_servico/list.html', context)


@login_required
def produto_servico_detail(request, pk):
    """Detalhes de um produto/serviço"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente = produto_servico.cliente
    
    # Campanhas relacionadas (se houver)
    campanhas_relacionadas = cliente.campanhas.filter(
        # Você pode adicionar lógica para relacionar campanhas específicas
        # com produtos/serviços se necessário
    )[:5]
    
    context = {
        'produto_servico': produto_servico,
        'cliente': cliente,
        'campanhas_relacionadas': campanhas_relacionadas,
        'completude': produto_servico.completude_percentual,
        'title': f'{produto_servico.get_tipo_display()}: {produto_servico.nome}'
    }
    
    return render(request, 'gestor/produto_servico/detail.html', context)


@login_required
def produto_servico_create(request, cliente_pk):
    """Criar novo produto/serviço"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    if request.method == 'POST':
        form = ProdutoServicoEventoForm(request.POST)
        if form.is_valid():
            produto_servico = form.save(commit=False)
            produto_servico.cliente = cliente
            produto_servico.created_by = request.user
            produto_servico.save()
            
            messages.success(
                request, 
                f'{produto_servico.get_tipo_display()} "{produto_servico.nome}" criado com sucesso!'
            )
            logger.info(f'Produto/serviço {produto_servico.nome} criado para cliente {cliente.nome_empresa} por {request.user.username}')
            
            return redirect('gestor:produto_servico_detail', pk=produto_servico.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProdutoServicoEventoForm()
        
        # Pré-selecionar tipo se vier da URL
        tipo_inicial = request.GET.get('tipo')
        if tipo_inicial in [choice[0] for choice in ProdutoServicoEvento.TIPO_CHOICES]:
            form.fields['tipo'].initial = tipo_inicial
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': f'Novo Produto/Serviço - {cliente.nome_empresa}',
        'subtitle': 'Cadastro de Produto/Serviço/Curso/Evento',
        'action': 'Criar'
    }
    
    return render(request, 'gestor/produto_servico/form.html', context)


@login_required
def produto_servico_update(request, pk):
    """Editar produto/serviço existente"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente = produto_servico.cliente
    
    if request.method == 'POST':
        form = ProdutoServicoEventoForm(request.POST, instance=produto_servico)
        if form.is_valid():
            produto_servico = form.save()
            
            messages.success(
                request, 
                f'{produto_servico.get_tipo_display()} "{produto_servico.nome}" atualizado com sucesso!'
            )
            logger.info(f'Produto/serviço {produto_servico.nome} atualizado por {request.user.username}')
            
            return redirect('gestor:produto_servico_detail', pk=produto_servico.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProdutoServicoEventoForm(instance=produto_servico)
    
    context = {
        'form': form,
        'produto_servico': produto_servico,
        'cliente': cliente,
        'title': f'Editar: {produto_servico.nome}',
        'subtitle': f'Edição de {produto_servico.get_tipo_display()}',
        'action': 'Atualizar'
    }
    
    return render(request, 'gestor/produto_servico/form.html', context)


@login_required
@require_http_methods(["POST"])
def produto_servico_delete(request, pk):
    """Excluir produto/serviço"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente = produto_servico.cliente
    
    # Verificar se tem campanhas relacionadas (se implementado)
    # campanhas_relacionadas = produto_servico.campanhas.count()
    # if campanhas_relacionadas > 0:
    #     messages.error(
    #         request,
    #         f'Não é possível excluir "{produto_servico.nome}" pois está relacionado a {campanhas_relacionadas} campanha(s).'
    #     )
    #     return redirect('gestor:produto_servico_detail', pk=pk)
    
    nome = produto_servico.nome
    tipo = produto_servico.get_tipo_display()
    cliente_pk = cliente.pk
    
    try:
        produto_servico.delete()
        
        messages.success(
            request, 
            f'{tipo} "{nome}" excluído com sucesso!'
        )
        
        logger.info(f'{tipo} {nome} excluído por {request.user.username}')
        
    except Exception as e:
        logger.error(f'Erro ao excluir produto/serviço {nome}: {e}')
        messages.error(
            request, 
            f'Erro ao excluir {tipo.lower()} "{nome}". Tente novamente ou contate o suporte.'
        )
        return redirect('gestor:produto_servico_detail', pk=pk)
    
    return redirect('gestor:produto_servico_list', cliente_pk=cliente_pk)


@login_required
@require_http_methods(["POST"])
def produto_servico_toggle_status(request, pk):
    """Ativar/desativar produto/serviço via AJAX"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    
    # Toggle status
    produto_servico.ativo = not produto_servico.ativo
    produto_servico.save()
    
    status_text = 'ativado' if produto_servico.ativo else 'desativado'
    
    messages.success(
        request, 
        f'{produto_servico.get_tipo_display()} "{produto_servico.nome}" {status_text} com sucesso!'
    )
    
    return JsonResponse({
        'success': True,
        'message': f'{produto_servico.get_tipo_display()} {status_text} com sucesso',
        'ativo': produto_servico.ativo,
        'status_display': 'Ativo' if produto_servico.ativo else 'Inativo'
    })


@login_required
def produto_servico_api_search(request):
    """API para busca de produtos/serviços (para autocomplete)"""
    
    term = request.GET.get('term', '')
    cliente_id = request.GET.get('cliente_id')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    produtos_servicos = ProdutoServicoEvento.objects.filter(
        Q(nome__icontains=term) |
        Q(descricao__icontains=term),
        ativo=True
    )
    
    if cliente_id:
        produtos_servicos = produtos_servicos.filter(cliente_id=cliente_id)
    
    produtos_servicos = produtos_servicos[:10]
    
    results = []
    for item in produtos_servicos:
        results.append({
            'id': str(item.pk),
            'text': item.nome,
            'tipo': item.get_tipo_display(),
            'tipo_code': item.tipo,
            'cliente': item.cliente.nome_empresa,
            'preco': float(item.preco) if item.preco else None,
            'ativo': item.ativo,
            'completude': item.completude_percentual
        })
    
    return JsonResponse({'results': results})


# ===== VIEWS PARA RELATÓRIOS E ESTATÍSTICAS =====

@login_required
def produto_servico_stats(request, cliente_pk):
    """Estatísticas de produtos/serviços de um cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    produtos_servicos = cliente.produtos_servicos.all()
    
    stats = {
        'total': produtos_servicos.count(),
        'ativos': produtos_servicos.filter(ativo=True).count(),
        'por_tipo': {},
        'com_preco': produtos_servicos.exclude(preco__isnull=True).count(),
        'completude_media': 0,
        'preco_medio': 0,
    }
    
    # Estatísticas por tipo
    for tipo_code, tipo_nome in ProdutoServicoEvento.TIPO_CHOICES:
        count = produtos_servicos.filter(tipo=tipo_code).count()
        stats['por_tipo'][tipo_code] = {
            'nome': tipo_nome,
            'count': count,
            'ativos': produtos_servicos.filter(tipo=tipo_code, ativo=True).count()
        }
    
    # Completude média
    if produtos_servicos.exists():
        completudes = [item.completude_percentual for item in produtos_servicos]
        stats['completude_media'] = sum(completudes) / len(completudes)
    
    # Preço médio
    produtos_com_preco = produtos_servicos.exclude(preco__isnull=True)
    if produtos_com_preco.exists():
        precos = [float(item.preco) for item in produtos_com_preco]
        stats['preco_medio'] = sum(precos) / len(precos)
    
    return JsonResponse(stats)


@login_required 
def produto_servico_duplicar(request, pk):
    """Duplicar produto/serviço existente"""
    
    produto_servico_original = get_object_or_404(ProdutoServicoEvento, pk=pk)
    
    if request.method == 'POST':
        # Criar cópia
        produto_servico_novo = ProdutoServicoEvento.objects.get(pk=pk)
        produto_servico_novo.pk = None  # Resetar PK para criar novo objeto
        produto_servico_novo.nome = f"{produto_servico_original.nome} (Cópia)"
        produto_servico_novo.created_by = request.user
        produto_servico_novo.save()
        
        messages.success(
            request, 
            f'{produto_servico_novo.get_tipo_display()} duplicado com sucesso! '
            f'Não esqueça de editar o nome e outras informações.'
        )
        
        return redirect('gestor:produto_servico_update', pk=produto_servico_novo.pk)
    
    context = {
        'produto_servico': produto_servico_original,
        'action': 'duplicar'
    }
    
    return render(request, 'gestor/produto_servico/confirm_duplicate.html', context)