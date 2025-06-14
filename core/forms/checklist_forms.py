# core/forms/checklist_forms.py - SEM PLACEHOLDERS

from django import forms
from core.models import ClienteChecklist

class ClienteChecklistForm(forms.ModelForm):
    """Formulário para checklist operacional de execução de campanhas"""
    
    class Meta:
        model = ClienteChecklist
        exclude = ['cliente', 'created_at', 'updated_at', 'updated_by']
        
        widgets = {
            # === REFERÊNCIAS E MATERIAIS ===
            'banco_imagens_videos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'responsavel_conteudo': forms.TextInput(attrs={'class': 'form-control'}),
            'acesso_criativos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pasta_materiais': forms.URLInput(attrs={'class': 'form-control'}),
            
            # === PERMISSÕES E ACESSOS META ===
            'liberacao_meta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'business_manager_ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dominio_verificado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pixel_instalado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'conversoes_api_ativas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acesso_conta_anuncios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # === GOOGLE ADS E FERRAMENTAS ===
            'conta_google_ads': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'search_console': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # === OBSERVAÇÕES ===
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        
        labels = {
            'banco_imagens_videos': 'Possui banco de imagens/vídeos dos produtos/serviços?',
            'responsavel_conteudo': 'Responsável pela geração de conteúdo interno',
            'acesso_criativos': 'Tem acesso a criativos já utilizados?',
            'pasta_materiais': 'Link da pasta com materiais',
            'liberacao_meta': 'Liberação Meta realizada com o cliente?',
            'business_manager_ativo': 'Business Manager ativo?',
            'dominio_verificado': 'Domínio verificado no Business Manager?',
            'pixel_instalado': 'Pixel do Facebook instalado?',
            'conversoes_api_ativas': 'Conversões API ativas?',
            'acesso_conta_anuncios': 'Acesso à conta de anúncios liberado?',
            'conta_google_ads': 'Conta no Google Ads criada/acessível?',
            'search_console': 'Google Search Console configurado?',
            'observacoes': 'Observações Gerais',
        }
        
        help_texts = {
            'responsavel_conteudo': 'Pessoa interna responsável por fotos, vídeos, stories, bastidores',
            'pasta_materiais': 'Link para Google Drive, Dropbox ou similar com materiais',
            'liberacao_meta': 'Cliente autorizou criação de anúncios no Meta Business',
            'business_manager_ativo': 'Business Manager configurado e funcional',
            'dominio_verificado': 'Domínio do site verificado no Business Manager',
            'pixel_instalado': 'Pixel instalado e funcionando no site',
            'conversoes_api_ativas': 'API de conversões configurada para iOS 14.5+',
            'acesso_conta_anuncios': 'Acesso de administrador à conta de anúncios',
            'conta_google_ads': 'Conta Google Ads criada e com acesso liberado',
            'search_console': 'Search Console vinculado ao Google Analytics',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Organizar campos por seções para melhor UX
        self.field_sections = {
            'materiais': [
                'banco_imagens_videos', 'responsavel_conteudo', 
                'acesso_criativos', 'pasta_materiais'
            ],
            'meta': [
                'liberacao_meta', 'business_manager_ativo', 'dominio_verificado',
                'pixel_instalado', 'conversoes_api_ativas', 'acesso_conta_anuncios'
            ],
            'google': [
                'conta_google_ads', 'search_console'
            ],
            'observacoes': [
                'observacoes'
            ]
        }

    def get_section_progress(self, section_name):
        """Calcula progresso de uma seção específica"""
        if not hasattr(self, 'field_sections') or section_name not in self.field_sections:
            return 0
        
        fields = self.field_sections[section_name]
        if section_name == 'observacoes':  # Seção de observações não conta para progresso
            return 100
        
        total_fields = len(fields)
        completed_fields = 0
        
        for field_name in fields:
            field_value = self.instance.__dict__.get(field_name) if self.instance else None
            if field_name in ['responsavel_conteudo', 'pasta_materiais']:
                # Campos de texto: considera completo se tem conteúdo
                if field_value and str(field_value).strip():
                    completed_fields += 1
            else:
                # Campos boolean: considera completo se True
                if field_value:
                    completed_fields += 1
        
        return (completed_fields / total_fields) * 100 if total_fields > 0 else 0