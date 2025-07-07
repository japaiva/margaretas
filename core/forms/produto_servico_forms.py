# core/forms/produto_servico_forms.py

from django import forms
from core.models.produto_servico import ProdutoServicoEvento
from core.utils.view_utils import DateAwareModelForm
from decimal import Decimal, InvalidOperation
import re

class ProdutoServicoEventoForm(DateAwareModelForm):
    """Formulário para Produtos/Serviços/Eventos"""
    
    # Campo monetário como CharField com validação customizada
    preco = forms.CharField(
        label='Preço (R$)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        help_text='Digite o valor em qualquer formato'
    )
    
    class Meta:
        model = ProdutoServicoEvento
        fields = [
            'tipo', 'nome', 'descricao', 'caracteristicas_beneficios',
            'preco', 'posicionamento_mercado', 'mensagens_materiais_marketing',
            'data_lancamento', 'cronograma_producao', 'pacotes_opcoes',
            'objetivos_venda', 'metas_especificas', 'formato', 'duracao',
            'agenda', 'palestrantes_instrutores', 'materiais_recursos', 'ativo'
        ]
        
        widgets = {
            # Campos básicos
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'required': True
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
            
            # Características e benefícios
            'caracteristicas_beneficios': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
            
            # Posicionamento
            'posicionamento_mercado': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            
            # Marketing
            'mensagens_materiais_marketing': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
            
            # Cronograma
            'data_lancamento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'cronograma_producao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            
            # Pacotes e objetivos
            'pacotes_opcoes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            'objetivos_venda': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            'metas_especificas': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            
            # Campos específicos para cursos/eventos
            'formato': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'duracao': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'agenda': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4
            }),
            'palestrantes_instrutores': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            'materiais_recursos': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3
            }),
            
            # Status
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'tipo': 'Tipo *',
            'nome': 'Nome *',
            'descricao': 'Descrição',
            'caracteristicas_beneficios': 'Características e Benefícios',
            'preco': 'Preço (R$)',
            'posicionamento_mercado': 'Posicionamento no Mercado',
            'mensagens_materiais_marketing': 'Mensagens e Materiais de Marketing',
            'data_lancamento': 'Data de Lançamento',
            'cronograma_producao': 'Cronograma para Produção e Distribuição',
            'pacotes_opcoes': 'Pacotes e Opções de Serviço',
            'objetivos_venda': 'Objetivos da Venda',
            'metas_especificas': 'Metas Específicas',
            'formato': 'Formato (Curso/Evento)',
            'duracao': 'Duração',
            'agenda': 'Agenda/Programação',
            'palestrantes_instrutores': 'Palestrantes e Instrutores',
            'materiais_recursos': 'Materiais e Recursos',
            'ativo': 'Produto/Serviço Ativo?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar funcionalidade de mostrar/esconder campos baseado no tipo
        self.fields['tipo'].widget.attrs['onchange'] = 'toggleFields(this.value)'
        
        # Organizar campos por seções para melhor UX
        self.field_sections = {
            'basicos': ['tipo', 'nome', 'descricao', 'ativo'],
            'caracteristicas': ['caracteristicas_beneficios', 'preco', 'posicionamento_mercado'],
            'marketing': ['mensagens_materiais_marketing', 'objetivos_venda', 'metas_especificas'],
            'cronograma': ['data_lancamento', 'cronograma_producao', 'pacotes_opcoes'],
            'curso_evento': ['formato', 'duracao', 'agenda', 'palestrantes_instrutores', 'materiais_recursos']
        }

    def clean_preco(self):
        """Limpa e converte o campo de preço"""
        value = self.cleaned_data.get('preco')
        converted = self._convert_money_value(value)
        
        if converted is None and value and value.strip():
            raise forms.ValidationError(
                'Por favor, insira um valor numérico válido para o preço. '
                'Exemplos: 100.00, 1000.50, 1.000,00'
            )
        
        return converted

    def clean_nome(self):
        """Validação específica para o nome obrigatório"""
        nome = self.cleaned_data.get('nome')
        if not nome or not nome.strip():
            raise forms.ValidationError('O nome é obrigatório.')
        return nome.strip()

    def _convert_money_value(self, value):
        """Função auxiliar para converter valores monetários"""
        if not value:
            return None
            
        # Converter para string e limpar
        value = str(value).strip()
        if value == '':
            return None
            
        # Remover símbolos monetários e espaços
        value = re.sub(r'[R$\s\xa0]', '', value)
        
        # Tratar formato brasileiro vs americano
        if ',' in value and '.' in value:
            if value.rindex(',') > value.rindex('.'):
                value = value.replace('.', '').replace(',', '.')
            else:
                value = value.replace(',', '')
        elif ',' in value:
            parts = value.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                value = value.replace(',', '.')
            else:
                value = value.replace(',', '')
        
        # Limpar caracteres inválidos
        value = re.sub(r'[^0-9.]', '', value)
        
        # Garantir que só tenha um ponto decimal
        if value.count('.') > 1:
            parts = value.split('.')
            value = ''.join(parts[:-1]) + '.' + parts[-1]
        
        try:
            return Decimal(value) if value else None
        except (InvalidOperation, ValueError):
            return None


class ProdutoServicoEventoFilterForm(forms.Form):
    """Formulário para filtros da lista de produtos/serviços"""
    
    TIPO_CHOICES = [('', 'Todos os tipos')] + ProdutoServicoEvento.TIPO_CHOICES
    STATUS_CHOICES = [
        ('', 'Todos'),
        ('ativo', 'Ativos'),
        ('inativo', 'Inativos'),
    ]
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Nome, descrição...'
        })
    )