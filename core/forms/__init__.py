# core/forms/__init__.py

"""
Módulo de formulários do Portal de Marketing Margaretas

Este arquivo centraliza todas as importações dos formulários para facilitar
o uso em views e templates.

Estrutura:
- base.py: Formulários de infraestrutura (Usuario, PerfilUsuario, Parametro)
- cliente.py: Formulários de marketing (Cliente, ProdutoServicoEvento, Campanha)
- wizard_forms.py: Formulários do wizard de cadastro detalhado de cliente
"""

# ===== IMPORTAÇÕES DA BASE =====
from .base import (
    # Formulários de usuário
    UsuarioForm,
    UsuarioCreationForm,
    PerfilUsuarioForm,
    
    # Formulários de configuração
    ParametroForm,
    ConfiguracoesForm,
    
    # Classes base e mixins
    BaseModelForm,
    UploadMixin,
    
    # Widgets customizados
    CustomDateInput,
    CustomDateTimeInput,
)

# ===== IMPORTAÇÕES DO CLIENTE/MARKETING =====
from .cliente import (
    # Formulários principais
    ClienteForm,
    ProdutoServicoEventoForm,
    CampanhaForm,
)

# ===== IMPORTAÇÕES DO WIZARD =====
from .wizard_forms import (
    # Formulários do wizard de cliente
    ClienteWizardStep1Form, # Adicionado
    ClienteWizardStep2Form,
    ClienteWizardStep3Form,
    ClienteWizardStep4Form,
    ClienteWizardStep5Form,
    ClienteWizardStep6Form, # Adicionado
)

# ===== LISTA DE EXPORTAÇÃO =====
__all__ = [
    # === FORMULÁRIOS BASE ===
    'UsuarioForm',
    'UsuarioCreationForm',
    'PerfilUsuarioForm',
    'ParametroForm',
    'ConfiguracoesForm',
    
    # === CLASSES BASE E MIXINS ===
    'BaseModelForm',
    'UploadMixin',
    
    # === WIDGETS CUSTOMIZADOS ===
    'CustomDateInput',
    'CustomDateTimeInput',
    
    # === FORMULÁRIOS DE MARKETING ===
    'ClienteForm',
    'ProdutoServicoEventoForm', 
    'CampanhaForm',
    
    # === FORMULÁRIOS DO WIZARD ===
    'ClienteWizardStep1Form', # Adicionado
    'ClienteWizardStep2Form',
    'ClienteWizardStep3Form',
    'ClienteWizardStep4Form',
    'ClienteWizardStep5Form',
    'ClienteWizardStep6Form', # Adicionado
]

# ===== SHORTCUTS PARA IMPORTAÇÃO FÁCIL =====

# Formulários mais usados
MAIN_FORMS = {
    'usuario': UsuarioForm,
    'perfil': PerfilUsuarioForm,
    'cliente': ClienteForm,
    'produto': ProdutoServicoEventoForm,
    'campanha': CampanhaForm,
    'configuracao': ConfiguracoesForm,
}

# Forms do wizard para facilitar acesso
WIZARD_FORMS = {
    'step1': ClienteWizardStep1Form, # Adicionado
    'step2': ClienteWizardStep2Form,
    'step3': ClienteWizardStep3Form,
    'step4': ClienteWizardStep4Form,
    'step5': ClienteWizardStep5Form,
    'step6': ClienteWizardStep6Form, # Adicionado
}

# Widgets mais usados
WIDGETS = {
    'date': CustomDateInput,
    'datetime': CustomDateTimeInput,
}

# ===== FUNÇÕES UTILITÁRIAS =====

def get_form(form_name):
    """
    Retorna um formulário pelo nome
    
    Usage:
        form_class = get_form('cliente')
        form = form_class()
    """
    return MAIN_FORMS.get(form_name.lower())

def get_wizard_form(step):
    """
    Retorna um formulário do wizard pelo step
    
    Usage:
        form_class = get_wizard_form('step1')
        form = form_class()
    """
    return WIZARD_FORMS.get(step.lower())

def get_widget(widget_name):
    """
    Retorna um widget pelo nome
    
    Usage:
        widget = get_widget('date')
    """
    return WIDGETS.get(widget_name.lower())

def list_available_forms():
    """
    Lista todos os formulários disponíveis
    
    Returns:
        dict: Dicionário com nomes e classes dos formulários
    """
    return {
        'main_forms': MAIN_FORMS.copy(),
        'wizard_forms': WIZARD_FORMS.copy(),
        'widgets': WIDGETS.copy()
    }

# ===== METADADOS DO MÓDULO =====
__version__ = '1.0.0'
__author__ = 'Portal Margaretas'
__description__ = 'Formulários do Portal de Marketing'

# ===== VALIDAÇÕES DE IMPORTAÇÃO =====
try:
    # Verificar se todas as importações foram bem-sucedidas
    _test_imports = [
        UsuarioForm, ClienteForm, CampanhaForm, 
        BaseModelForm, CustomDateInput,
        ClienteWizardStep1Form, # Adicionado
        ClienteWizardStep2Form,
        ClienteWizardStep6Form # Adicionado
    ]
    
    # Log de sucesso (opcional)
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"✅ Formulários carregados com sucesso: {len(__all__)} classes")
    
except ImportError as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Erro ao importar formulários: {str(e)}")
    raise

# ===== CONFIGURAÇÕES PADRÃO =====

# Configurações padrão para widgets
DEFAULT_WIDGET_ATTRS = {
    'text': {'class': 'form-control'},
    'select': {'class': 'form-select'},
    'checkbox': {'class': 'form-check-input'},
    'file': {'class': 'form-control'},
}

# Mensagens de erro padrão em português
DEFAULT_ERROR_MESSAGES = {
    'required': 'Este campo é obrigatório.',
    'invalid': 'Digite um valor válido.',
    'max_length': 'Certifique-se de que este valor tenha no máximo %(limit_value)d caracteres.',
    'min_length': 'Certifique-se de que este valor tenha pelo menos %(limit_value)d caracteres.',
}

# ===== CONFIGURAÇÃO PARA DJANGO =====

# Para uso em settings.py se necessário
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'