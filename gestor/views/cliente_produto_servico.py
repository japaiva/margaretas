# gestor/views/cliente_produtos_servicos.py - VIEWS DE PRODUTOS/SERVIÇOS INLINE

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.db.models import Q
from decimal import Decimal

from core.models import Cliente, ProdutoServicoEvento
from core.forms.produto_servico_forms import ProdutoServicoEventoForm

import logging
logger = logging.getLogger(__name__)


# ===== VIEWS INLINE PARA PRODUTOS/SERVIÇOS =====

@login_required
def produto_servico_create_inline(request, cliente_pk):
    """Criar produto/serviço inline no detalhe do cliente"""
    
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
                f'✅ {produto_servico.get_tipo_display()} "{produto_servico.nome}" criado com sucesso!'
            )
            logger.info(f'Produto/serviço {produto_servico.nome} criado para cliente {cliente.nome_empresa}')
            
            # ✅ CORREÇÃO: Sempre retornar para o detalhe do cliente
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = ProdutoServicoEventoForm()
        
        # Pré-selecionar tipo se vier da URL
        tipo_inicial = request.GET.get('tipo')
        if tipo_inicial in [choice[0] for choice in ProdutoServicoEvento.TIPO_CHOICES]:
            form.fields['tipo'].initial = tipo_inicial
    
    # Definir título dinâmico baseado no tipo (se vier da URL) ou genérico
    tipo_inicial = form.fields['tipo'].initial
    if tipo_inicial:
        tipo_display = dict(ProdutoServicoEvento.TIPO_CHOICES).get(tipo_inicial, 'Item')
        title = f'Novo {tipo_display} - {cliente.nome_empresa}'
    else:
        title = f'Novo Item - {cliente.nome_empresa}'
    
    context = {
        'form': form,
        'cliente': cliente,
        'title': title,
        'action': 'Criar',
        'is_inline': True,
        'cancel_url': reverse('gestor:cliente_detail', args=[cliente.pk]),
    }
    
    return render(request, 'gestor/produto_servico/form_inline.html', context)


@login_required
def produto_servico_update_inline(request, pk):
    """Editar produto/serviço inline"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente = produto_servico.cliente
    
    if request.method == 'POST':
        form = ProdutoServicoEventoForm(request.POST, instance=produto_servico)
        if form.is_valid():
            produto_servico = form.save()
            
            messages.success(
                request,
                f'✅ {produto_servico.get_tipo_display()} "{produto_servico.nome}" atualizado com sucesso!'
            )
            logger.info(f'Produto/serviço {produto_servico.nome} atualizado')
            
            # ✅ CORREÇÃO: Sempre retornar para o detalhe do cliente
            return redirect('gestor:cliente_detail', pk=cliente.pk)
        else:
            messages.error(request, '❌ Por favor, corrija os erros no formulário.')
    else:
        form = ProdutoServicoEventoForm(instance=produto_servico)
    
    context = {
        'form': form,
        'produto_servico': produto_servico,
        'cliente': cliente,
        'title': f'Editar {produto_servico.get_tipo_display()}: {produto_servico.nome}',
        'action': 'Atualizar',
        'is_inline': True,
        'cancel_url': reverse('gestor:cliente_detail', args=[cliente.pk]),
    }
    
    return render(request, 'gestor/produto_servico/form_inline.html', context)


@login_required
@require_http_methods(["POST"])
def produto_servico_delete_inline(request, pk):
    """Excluir produto/serviço inline"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    cliente = produto_servico.cliente
    
    nome = produto_servico.nome
    tipo = produto_servico.get_tipo_display()
    
    try:
        produto_servico.delete()
        
        messages.success(
            request,
            f'✅ {tipo} "{nome}" excluído com sucesso!'
        )
        
        logger.info(f'{tipo} {nome} excluído do cliente {cliente.nome_empresa}')
        
    except Exception as e:
        logger.error(f'Erro ao excluir produto/serviço {nome}: {e}')
        messages.error(
            request,
            f'❌ Erro ao excluir {tipo.lower()} "{nome}". Tente novamente.'
        )
    
    # ✅ CORREÇÃO: Sempre retornar para o detalhe do cliente
    return redirect('gestor:cliente_detail', pk=cliente.pk)


@login_required
@require_http_methods(["POST"])
def produto_servico_toggle_status_inline(request, pk):
    """Toggle status via AJAX inline"""
    
    produto_servico = get_object_or_404(ProdutoServicoEvento, pk=pk)
    
    # Toggle status
    produto_servico.ativo = not produto_servico.ativo
    produto_servico.save()
    
    status_text = 'ativado' if produto_servico.ativo else 'desativado'
    
    logger.info(f'Status do {produto_servico.get_tipo_display()} {produto_servico.nome} alterado para {status_text}')
    
    return JsonResponse({
        'success': True,
        'message': f'{produto_servico.get_tipo_display()} {status_text} com sucesso',
        'ativo': produto_servico.ativo,
        'status_display': 'Ativo' if produto_servico.ativo else 'Inativo'
    })


# ===== VIEWS DE RESPOSTA RÁPIDA PARA PRODUTOS/SERVIÇOS =====

@login_required
def produto_servico_quick_create(request, cliente_pk):
    """Criação rápida de produto/serviço via modal/AJAX"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    
    if request.method == 'POST':
        # Dados mínimos para criação rápida
        nome = request.POST.get('nome', '').strip()
        tipo = request.POST.get('tipo', '')
        preco = request.POST.get('preco', '')
        
        if not nome:
            return JsonResponse({'success': False, 'message': 'Nome é obrigatório'})
        
        if tipo not in [choice[0] for choice in ProdutoServicoEvento.TIPO_CHOICES]:
            return JsonResponse({'success': False, 'message': 'Tipo inválido'})
        
        try:
            produto_servico = ProdutoServicoEvento.objects.create(
                cliente=cliente,
                nome=nome,
                tipo=tipo,
                preco=Decimal(preco) if preco else None,
                created_by=request.user
            )
            
            logger.info(f'Produto/serviço rápido {produto_servico.nome} criado para cliente {cliente.nome_empresa}')
            
            return JsonResponse({
                'success': True,
                'message': f'✅ {produto_servico.get_tipo_display()} criado com sucesso!',
                'produto_servico': {
                    'id': str(produto_servico.pk),
                    'nome': produto_servico.nome,
                    'tipo': produto_servico.get_tipo_display(),
                    'preco': float(produto_servico.preco) if produto_servico.preco else None,
                    'ativo': produto_servico.ativo
                }
            })
            
        except Exception as e:
            logger.error(f'Erro ao criar produto/serviço rápido: {e}')
            return JsonResponse({'success': False, 'message': 'Erro ao criar produto/serviço'})
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


# ===== VIEWS PARA RELATÓRIOS E ESTATÍSTICAS =====

@login_required
def cliente_produtos_servicos_stats(request, cliente_pk):
    """API para estatísticas de produtos/serviços do cliente"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    produtos_servicos = cliente.produtos_servicos.all()
    
    stats = {
        'total': produtos_servicos.count(),
        'ativos': produtos_servicos.filter(ativo=True).count(),
        'inativos': produtos_servicos.filter(ativo=False).count(),
        'por_tipo': {},
        'com_preco': produtos_servicos.exclude(preco__isnull=True).count(),
        'completude_media': 0,
        'preco_medio': 0,
    }
    
    # Estatísticas por tipo
    for tipo_code, tipo_nome in ProdutoServicoEvento.TIPO_CHOICES:
        count = produtos_servicos.filter(tipo=tipo_code).count()
        ativos = produtos_servicos.filter(tipo=tipo_code, ativo=True).count()
        stats['por_tipo'][tipo_code] = {
            'nome': tipo_nome,
            'count': count,
            'ativos': ativos,
            'inativos': count - ativos
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
def produto_servico_api_search_cliente(request, cliente_pk):
    """API para busca de produtos/serviços de um cliente específico"""
    
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    term = request.GET.get('term', '')
    
    if len(term) < 2:
        return JsonResponse({'results': []})
    
    produtos_servicos = cliente.produtos_servicos.filter(
        Q(nome__icontains=term) |
        Q(descricao__icontains=term),
        ativo=True
    )[:10]
    
    results = []
    for item in produtos_servicos:
        results.append({
            'id': str(item.pk),
            'text': item.nome,
            'tipo': item.get_tipo_display(),
            'tipo_code': item.tipo,
            'preco': float(item.preco) if item.preco else None,
            'ativo': item.ativo,
            'completude': item.completude_percentual
        })
    
    return JsonResponse({'results': results})