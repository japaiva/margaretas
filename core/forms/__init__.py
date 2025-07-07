# core/forms/__init__.py

"""
Módulo de formulários do Portal de Marketing Margaretas

Estrutura:
- base.py: Formulários de infraestrutura (Usuario, PerfilUsuario, Parametro)
- cliente.py: Formulários básicos (Cliente, Campanha)
- produto_servico_forms.py: Formulários para Produtos/Serviços/Eventos
- wizard_forms.py: Formulários do wizard de briefing (4 steps)
- checklist_forms.py: Formulário de checklist operacional
"""

# ===== IMPORTAÇÕES DA BASE =====
from .base import (
    UsuarioForm,
    UsuarioCreationForm,
    PerfilUsuarioForm,
    ParametroForm,
    ConfiguracoesForm,
    BaseModelForm,
    UploadMixin,
    CustomDateInput,
    CustomDateTimeInput,
)

# ===== IMPORTAÇÕES DO CLIENTE/MARKETING =====
from .cliente import (
    ClienteForm,
    CampanhaForm,
)

# ===== IMPORTAÇÕES DE PRODUTOS/SERVIÇOS =====
from .produto_servico_forms import (
    ProdutoServicoEventoForm,
    ProdutoServicoEventoFilterForm,
)

# ===== IMPORTAÇÕES DO WIZARD =====
from .wizard_forms import (
    ClienteWizardStep1Form,
    ClienteWizardStep2Form,
    ClienteWizardStep3Form,
    ClienteWizardStep4Form,
    ClienteWizardConfirmForm,
)

# ===== IMPORTAÇÕES DO CHECKLIST =====
from .checklist_forms import (
    ClienteChecklistForm,
)

# ===== LISTA DE EXPORTAÇÃO ATUALIZADA =====
__all__ = [
    # Formulários base/infraestrutura
    'UsuarioForm', 
    'UsuarioCreationForm', 
    'PerfilUsuarioForm', 
    'ParametroForm', 
    'ConfiguracoesForm', 
    'BaseModelForm', 
    'UploadMixin', 
    'CustomDateInput', 
    'CustomDateTimeInput',
    
    # Formulários básicos de marketing
    'ClienteForm', 
    'CampanhaForm',
    
    # Formulários de produtos/serviços/eventos
    'ProdutoServicoEventoForm',
    'ProdutoServicoEventoFilterForm',
    
    # Formulários do wizard de briefing (4 steps)
    'ClienteWizardStep1Form',    # Público-Alvo
    'ClienteWizardStep2Form',    # Posicionamento e Comunicação
    'ClienteWizardStep3Form',    # Objetivos e Estratégia
    'ClienteWizardStep4Form',    # Recursos e Expectativas
    'ClienteWizardConfirmForm',  # Confirmação final
    
    # Formulário operacional
    'ClienteChecklistForm',
]