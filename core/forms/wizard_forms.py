# core/forms/wizard_forms.py - VERSÃO REFATORADA (5 STEPS) COM NOVA ABA HISTÓRIA

from django import forms
from core.models import Cliente
from decimal import Decimal, InvalidOperation
import re

class ClienteWizardStep1Form(forms.ModelForm):
    """Step 1: História da Empresa (NOVA ABA)"""
    
    class Meta:
        model = Cliente
        fields = [
            'historia_empresa', 'missao', 'visao', 'valores'
        ]
        
        widgets = {
            'historia_empresa': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'missao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'visao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'valores': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        labels = {
            'historia_empresa': 'História da Empresa *',
            'missao': 'Missão da Empresa',
            'visao': 'Visão da Empresa', 
            'valores': 'Valores da Empresa',
        }

    def clean_historia_empresa(self):
        value = self.cleaned_data.get('historia_empresa')
        if not value or len(value.strip()) < 20:
            raise forms.ValidationError('A história da empresa deve ter pelo menos 20 caracteres.')
        return value

    def clean_missao(self):
        value = self.cleaned_data.get('missao')
        if value and len(value.strip()) < 10:
            raise forms.ValidationError('A missão deve ter pelo menos 10 caracteres.')
        return value

    def clean_visao(self):
        value = self.cleaned_data.get('visao')
        if value and len(value.strip()) < 10:
            raise forms.ValidationError('A visão deve ter pelo menos 10 caracteres.')
        return value


class ClienteWizardStep2Form(forms.ModelForm):
    """Step 2: Posicionamento e Comunicação"""
    
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
        help_text="Selecione até 3 opções que melhor representam a personalidade da marca"
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

    def clean_posicionamento_atual(self):
        value = self.cleaned_data.get('posicionamento_atual')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Posicionamento atual deve ter pelo menos 5 caracteres.')
        return value

    def clean_objetivos_posicionamento(self):
        value = self.cleaned_data.get('objetivos_posicionamento')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Objetivos de posicionamento devem ter pelo menos 5 caracteres.')
        return value

    def clean_tom_voz(self):
        value = self.cleaned_data.get('tom_voz')
        if value and len(value.strip()) < 3:
            raise forms.ValidationError('Tom e voz deve ter pelo menos 3 caracteres.')
        return value

    def clean_mensagem_principal(self):
        value = self.cleaned_data.get('mensagem_principal')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Mensagem principal deve ter pelo menos 5 caracteres.')
        return value

    def clean_canais_comunicacao(self):
        value = self.cleaned_data.get('canais_comunicacao')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Canais de comunicação devem ter pelo menos 5 caracteres.')
        return value


class ClienteWizardStep3Form(forms.ModelForm):
    """Step 3: Objetivos e Estratégia"""
    
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

    def clean_objetivos_marketing(self):
        value = self.cleaned_data.get('objetivos_marketing')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Objetivos de marketing devem ter pelo menos 5 caracteres.')
        return value

    def clean_metas_especificas(self):
        value = self.cleaned_data.get('metas_especificas')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Metas específicas devem ter pelo menos 5 caracteres.')
        return value

    def clean_kpis_empresa(self):
        value = self.cleaned_data.get('kpis_empresa')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('KPIs da empresa devem ter pelo menos 5 caracteres.')
        return value

    def clean_analise_concorrencia(self):
        value = self.cleaned_data.get('analise_concorrencia')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Análise da concorrência deve ter pelo menos 5 caracteres.')
        return value

    def clean_pontos_fortes_fracos_concorrencia(self):
        value = self.cleaned_data.get('pontos_fortes_fracos_concorrencia')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Pontos fortes e fracos da concorrência devem ter pelo menos 5 caracteres.')
        return value


class ClienteWizardStep4Form(forms.ModelForm):
    """Step 4: Público-Alvo"""
    
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

    def clean_descricao_publico(self):
        value = self.cleaned_data.get('descricao_publico')
        if value and len(value.strip()) < 10:
            raise forms.ValidationError('Descrição do público deve ter pelo menos 10 caracteres.')
        return value

    def clean_necessidades_desejos(self):
        value = self.cleaned_data.get('necessidades_desejos')
        if value and len(value.strip()) < 10:
            raise forms.ValidationError('Necessidades e desejos devem ter pelo menos 10 caracteres.')
        return value

    def clean_comportamento_compra(self):
        value = self.cleaned_data.get('comportamento_compra')
        if value and len(value.strip()) < 10:
            raise forms.ValidationError('Comportamento de compra deve ter pelo menos 10 caracteres.')
        return value


class ClienteWizardStep5Form(forms.ModelForm):
    """Step 5: Recursos e Expectativas (Final)"""
    
    # Campo monetário como CharField
    orcamento_marketing = forms.CharField(
        label='Orçamento de Marketing (R$)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
            raise forms.ValidationError('Valor inválido para orçamento de marketing')

    def clean_equipe_marketing(self):
        value = self.cleaned_data.get('equipe_marketing')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Equipe de marketing deve ter pelo menos 5 caracteres.')
        return value

    def clean_recursos_tecnologicos(self):
        value = self.cleaned_data.get('recursos_tecnologicos')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Recursos tecnológicos devem ter pelo menos 5 caracteres.')
        return value

    def clean_expectativas_agencia(self):
        value = self.cleaned_data.get('expectativas_agencia')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Expectativas da agência devem ter pelo menos 5 caracteres.')
        return value

    def clean_resultados_esperados(self):
        value = self.cleaned_data.get('resultados_esperados')
        if value and len(value.strip()) < 5:
            raise forms.ValidationError('Resultados esperados devem ter pelo menos 5 caracteres.')
        return value


# Formulário para confirmação final
class ClienteWizardConfirmForm(forms.Form):
    """Formulário de confirmação final - usado no último step"""
    
    confirmar_dados = forms.BooleanField(
        required=True,
        label="Confirmo que todas as informações do briefing estão corretas",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    observacoes_finais = forms.CharField(
        required=False,
        label="Observações Finais",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )