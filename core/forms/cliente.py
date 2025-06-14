# core/forms/cliente.py - VERSÃO CORRIGIDA E SIMPLIFICADA

from django import forms
from core.models import Cliente, Campanha  # ❌ REMOVIDO: ProdutoServicoEvento
from core.utils.view_utils import DateAwareModelForm
from decimal import Decimal, InvalidOperation
import re


class ClienteForm(DateAwareModelForm):
    """Formulário SIMPLES para cadastro rápido de clientes - APENAS DADOS BÁSICOS"""
    
    # Campos monetários como CharField com validação customizada
    faturamento_anual = forms.CharField(
        label='Faturamento Anual Estimado (R$)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1.000.000,00'
        }),
        help_text='Digite o valor em qualquer formato'
    )
    
    class Meta:
        model = Cliente
        fields = [
            # === DADOS BÁSICOS (OBRIGATÓRIO APENAS NOME) ===
            'nome_empresa', 'ativo',
            
            # === INFORMAÇÕES DA EMPRESA ===
            'cnpj_cpf', 'endereco_completo', 'historia_empresa', 
            'missao', 'visao', 'valores', 'lista_produtos_servicos',
            
            # === RESPONSÁVEIS E CONTATOS ===
            'responsavel_contrato', 'cargo_responsavel', 'contato_responsavel',
            'pessoa_contato_tecnico', 'contato_tecnico',
            
            # === INFORMAÇÕES FINANCEIRAS ===
            'faturamento_anual',
            
            # === INFORMAÇÕES DIGITAIS BÁSICAS ===
            'website_principal', 'outros_dominios', 'crm_utilizado',
            'google_analytics', 'tag_manager', 'pixel_facebook',
            
            # === CONTEXTO ADICIONAL ===
            'principais_desafios', 'sazonalidades', 'certificacoes_diferenciais'
        ]
        
        widgets = {
            # === CAMPO OBRIGATÓRIO ===
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome da empresa ou marca',
                'required': True
            }),
            
            # === INFORMAÇÕES BÁSICAS ===
            'cnpj_cpf': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '00.000.000/0000-00 ou 000.000.000-00'
            }),
            'endereco_completo': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Endereço completo da empresa'
            }),
            
            # === HISTÓRICO DA EMPRESA ===
            'historia_empresa': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, 
                'placeholder': 'Conte a história da empresa, marcos importantes...'
            }),
            'missao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Qual é a missão da empresa?'
            }),
            'visao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Qual é a visão da empresa?'
            }),
            'valores': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Quais são os valores da empresa?'
            }),
            'lista_produtos_servicos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4, 
                'placeholder': 'Descreva os produtos ou serviços oferecidos'
            }),
            
            # === RESPONSÁVEIS ===
            'responsavel_contrato': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome completo'
            }),
            'cargo_responsavel': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cargo na empresa'
            }),
            'contato_responsavel': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email ou telefone'
            }),
            'pessoa_contato_tecnico': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome completo'
            }),
            'contato_tecnico': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email ou telefone'
            }),
            
            # === DIGITAL ===
            'website_principal': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com.br'
            }),
            'outros_dominios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2, 
                'placeholder': 'Outros sites ou domínios da empresa'
            }),
            'crm_utilizado': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Pipedrive, Salesforce, RD Station'
            }),
            
            # === CONTEXTO ADICIONAL ===
            'principais_desafios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Principais desafios do mercado atual'
            }),
            'sazonalidades': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Períodos de alta/baixa, datas importantes'
            }),
            'certificacoes_diferenciais': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3, 
                'placeholder': 'Certificações, prêmios, diferenciais técnicos'
            }),
            
            # === CHECKBOXES ===
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'google_analytics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tag_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pixel_facebook': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            # ÚNICO CAMPO OBRIGATÓRIO
            'nome_empresa': 'Nome da Empresa/Marca *',
            
            # TODOS OS OUTROS SÃO OPCIONAIS
            'ativo': 'Cliente Ativo?',
            'cnpj_cpf': 'CNPJ/CPF',
            'endereco_completo': 'Endereço Completo',
            'historia_empresa': 'História da Empresa',
            'missao': 'Missão da Empresa',
            'visao': 'Visão da Empresa',
            'valores': 'Valores da Empresa',
            'lista_produtos_servicos': 'Produtos ou Serviços',
            'responsavel_contrato': 'Responsável pelo Contrato',
            'cargo_responsavel': 'Cargo do Responsável',
            'contato_responsavel': 'Contato do Responsável',
            'pessoa_contato_tecnico': 'Pessoa de Contato Técnico',
            'contato_tecnico': 'Contato da Pessoa Técnica',
            'faturamento_anual': 'Faturamento Anual Estimado (R$)',
            'website_principal': 'Website Principal',
            'outros_dominios': 'Outros Domínios',
            'crm_utilizado': 'CRM Utilizado',
            'google_analytics': 'Google Analytics Configurado?',
            'tag_manager': 'Google Tag Manager Configurado?',
            'pixel_facebook': 'Pixel do Facebook Instalado?',
            'principais_desafios': 'Principais Desafios do Mercado',
            'sazonalidades': 'Sazonalidades do Negócio',
            'certificacoes_diferenciais': 'Certificações ou Diferenciais',
        }

    def clean_faturamento_anual(self):
        """Limpa e converte o campo de faturamento anual"""
        value = self.cleaned_data.get('faturamento_anual')
        converted = self._convert_money_value(value)
        
        if converted is None and value and value.strip():
            raise forms.ValidationError(
                'Por favor, insira um valor numérico válido para o faturamento anual. '
                'Exemplos: 1000000, 1000000.50, 1.000.000,50'
            )
        
        return converted

    def clean_nome_empresa(self):
        """Validação específica para o único campo obrigatório"""
        nome = self.cleaned_data.get('nome_empresa')
        if not nome or not nome.strip():
            raise forms.ValidationError('O nome da empresa é obrigatório.')
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


class CampanhaForm(DateAwareModelForm):
    """Formulário SIMPLIFICADO para campanhas"""
    
    class Meta:
        model = Campanha
        fields = [
            # === IDENTIFICAÇÃO ===
            'nome_campanha', 'descricao', 'status',
            
            # === OBJETIVOS ===
            'objetivo_principal', 'kpis_campanha',
            
            # === PÚBLICO-ALVO ===
            'publico_alvo',
            
            # === ORÇAMENTO E CRONOGRAMA ===
            'orcamento_total', 'data_inicio', 'data_termino',
        ]
        
        widgets = {
            # Identificação
            'nome_campanha': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome da campanha'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Descrição da campanha'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            
            # Objetivos
            'objetivo_principal': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Qual o objetivo principal da campanha?'
            }),
            'kpis_campanha': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'KPIs para medir sucesso da campanha'
            }),
            
            # Público-alvo
            'publico_alvo': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Descrição do público-alvo específico desta campanha'
            }),
            
            # Orçamento e cronograma
            'orcamento_total': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'placeholder': 'Ex: 10000.00'
            }),
            'data_inicio': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'data_termino': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
        }
        
        labels = {
            'nome_campanha': 'Nome da Campanha *',
            'descricao': 'Descrição',
            'status': 'Status',
            'objetivo_principal': 'Objetivo Principal *',
            'kpis_campanha': 'KPIs da Campanha *',
            'publico_alvo': 'Público-Alvo da Campanha *',
            'orcamento_total': 'Orçamento Total (R$) *',
            'data_inicio': 'Data de Início *',
            'data_termino': 'Data de Término *',
        }

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_termino = cleaned_data.get('data_termino')
        
        if data_inicio and data_termino:
            if data_termino <= data_inicio:
                raise forms.ValidationError("A data de término deve ser posterior à data de início.")
        
        return cleaned_data