# core/forms/wizard_forms.py - VERSÃO CORRIGIDA

from django import forms
from core.models import Cliente
from decimal import Decimal, InvalidOperation
import re

class ClienteWizardStep1Form(forms.ModelForm):
    """Passo 1: Informações Básicas"""
    
    # Campo monetário como CharField com validação customizada
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
            'nome_empresa', 'ativo', 'cnpj_cpf', 'endereco_completo',
            'responsavel_contrato', 'cargo_responsavel', 'contato_responsavel',
            'pessoa_contato_tecnico', 'contato_tecnico', 'faturamento_anual',
            'lista_produtos_servicos', 'website_principal', 'outros_dominios'
        ]
        
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cnpj_cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco_completo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsavel_contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'pessoa_contato_tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'contato_tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'lista_produtos_servicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'website_principal': forms.URLInput(attrs={'class': 'form-control'}),
            'outros_dominios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_faturamento_anual(self):
        """Converter valor monetário para Decimal"""
        value = self.cleaned_data.get('faturamento_anual')
        if not value:
            return None
            
        # Remover símbolos e converter
        value = re.sub(r'[R$\s\xa0]', '', value.strip())
        
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
        
        try:
            return Decimal(value) if value else None
        except (InvalidOperation, ValueError):
            raise forms.ValidationError('Valor inválido para faturamento anual')


class ClienteWizardStep2Form(forms.ModelForm):
    """Passo 2: Público-Alvo"""
    
    class Meta:
        model = Cliente
        fields = [
            'descricao_publico', 'necessidades_desejos', 'comportamento_compra',
            'consideracoes_demograficas', 'niveis_consciencia', 
            'objecoes_comuns', 'tentativas_passadas'
        ]
        
        widgets = {
            'descricao_publico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'necessidades_desejos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comportamento_compra': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'consideracoes_demograficas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'niveis_consciencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objecoes_comuns': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tentativas_passadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ClienteWizardStep3Form(forms.ModelForm):
    """Passo 3: Posicionamento e Comunicação"""
    
    ARQUETIPOS_CHOICES = [
        ('mestre_sabio', 'Um mestre sábio'),
        ('rebelde_provocador', 'Um rebelde provocador'),
        ('cuidador_acolhedor', 'Um cuidador acolhedor'),
        ('heroi_determinado', 'Um herói determinado'),
        ('artista_criativo', 'Um artista criativo'),
        ('explorador_curioso', 'Um explorador curioso'),
    ]
    
    arquetipos = forms.MultipleChoiceField(
        choices=ARQUETIPOS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Selecione até 3 opções"
    )
    
    class Meta:
        model = Cliente
        fields = [
            'posicionamento_atual', 'objetivos_posicionamento', 'diferenciacao',
            'tom_voz', 'mensagem_principal', 'manifesto_marca', 
            'canais_comunicacao', 'manual_marca', 'arquetipos'
        ]
        
        widgets = {
            'posicionamento_atual': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objetivos_posicionamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diferenciacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tom_voz': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mensagem_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manifesto_marca': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'canais_comunicacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'manual_marca': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_arquetipos(self):
        """Validar máximo 3 arquétipos"""
        arquetipos = self.cleaned_data.get('arquetipos', [])
        if len(arquetipos) > 3:
            raise forms.ValidationError("Selecione no máximo 3 arquétipos.")
        return arquetipos


class ClienteWizardStep4Form(forms.ModelForm):
    """Passo 4: Objetivos e Estratégia"""
    
    class Meta:
        model = Cliente
        fields = [
            'objetivos_marketing', 'metas_especificas', 'kpis_empresa',
            'analise_concorrencia', 'pontos_fortes_fracos_concorrencia'
        ]
        
        widgets = {
            'objetivos_marketing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'metas_especificas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'kpis_empresa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'analise_concorrencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pontos_fortes_fracos_concorrencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ClienteWizardStep5Form(forms.ModelForm):
    """Passo 5: Recursos e Expectativas"""
    
    # Campo monetário como CharField
    orcamento_marketing = forms.CharField(
        label='Orçamento de Marketing (R$)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50.000,00'
        }),
        help_text='Digite o valor em qualquer formato'
    )
    
    class Meta:
        model = Cliente
        fields = [
            'orcamento_marketing', 'equipe_marketing', 'recursos_tecnologicos',
            'expectativas_agencia', 'resultados_esperados',
            'experiencia_agencias', 'criativos_performaram', 
            'analise_campanhas_anteriores', 'google_analytics', 
            'tag_manager', 'pixel_facebook', 'crm_utilizado',
            'principais_desafios', 'sazonalidades', 'certificacoes_diferenciais'
        ]
        
        widgets = {
            'equipe_marketing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recursos_tecnologicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'expectativas_agencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'resultados_esperados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experiencia_agencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'criativos_performaram': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'analise_campanhas_anteriores': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'google_analytics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tag_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pixel_facebook': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'crm_utilizado': forms.TextInput(attrs={'class': 'form-control'}),
            'principais_desafios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sazonalidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'certificacoes_diferenciais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_orcamento_marketing(self):
        """Converter valor monetário para Decimal"""
        value = self.cleaned_data.get('orcamento_marketing')
        if not value:
            return None
            
        # Mesma lógica do faturamento_anual
        value = re.sub(r'[R$\s\xa0]', '', value.strip())
        
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
        
        try:
            return Decimal(value) if value else None
        except (InvalidOperation, ValueError):
            raise forms.ValidationError('Valor inválido para orçamento de marketing')


class ClienteWizardStep6Form(forms.Form):
    """Passo 6: Revisão Final - Só confirmação"""
    
    confirmar_dados = forms.BooleanField(
        required=True,
        label="Confirmo que todas as informações estão corretas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    observacoes_finais = forms.CharField(
        required=False,
        label="Observações Finais",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Alguma observação adicional ou informação importante?'
        })
    )