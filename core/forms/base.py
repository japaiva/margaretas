# core/forms/base.py

from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from core.models.base import Usuario, PerfilUsuario, Parametro


# ===== FORMULÁRIOS DE USUÁRIO =====

class UsuarioForm(forms.ModelForm):
    """Formulário para cadastro e edição de usuários"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Senha",
        help_text="Deixe em branco para manter a senha atual"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label="Confirmar Senha"
    )
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'nivel', 'telefone', 'is_active', 'is_staff'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário único'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primeiro nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'data-mask': '(00) 00000-0000'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'username': 'Nome de Usuário *',
            'first_name': 'Primeiro Nome *',
            'last_name': 'Sobrenome',
            'email': 'E-mail *',
            'nivel': 'Nível de Acesso *',
            'telefone': 'Telefone',
            'is_active': 'Usuário Ativo?',
            'is_staff': 'Acesso ao Admin?',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se estiver editando um usuário existente, não exigir senha
        if self.instance.pk:
            self.fields['password'].required = False
            self.fields['confirm_password'].required = False
            self.fields['password'].help_text = "Deixe em branco para manter a senha atual"
        else:
            self.fields['password'].required = True
            self.fields['confirm_password'].required = True
            self.fields['password'].help_text = "Mínimo 8 caracteres"
        
        # Marcar campos obrigatórios
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['nivel'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        # Validar senhas
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")
        
        if password and len(password) < 8:
            self.add_error('password', "A senha deve ter pelo menos 8 caracteres.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Se uma senha foi fornecida, codificá-la
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password)
        
        if commit:
            user.save()
        
        return user


class UsuarioCreationForm(UserCreationForm):
    """Formulário específico para criação de usuários"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nivel = forms.ChoiceField(
        choices=Usuario.NIVEL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    telefone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-mask': '(00) 00000-0000'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'nivel', 'telefone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        user.nivel = self.cleaned_data['nivel']
        user.telefone = self.cleaned_data.get('telefone', '')
        
        if commit:
            user.save()
        
        return user


# ===== FORMULÁRIO DE PERFIL =====

class PerfilUsuarioForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'telefone', 'nivel', 'foto', 'bio', 'data_nascimento',
            'receber_emails', 'receber_sms'
        ]
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999',
                'data-mask': '(00) 00000-0000'
            }),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre você...'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'receber_emails': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'receber_sms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'telefone': 'Telefone',
            'nivel': 'Nível de Acesso',
            'foto': 'Foto do Perfil',
            'bio': 'Biografia',
            'data_nascimento': 'Data de Nascimento',
            'receber_emails': 'Receber notificações por e-mail',
            'receber_sms': 'Receber notificações por SMS',
        }
        help_texts = {
            'foto': 'Formatos aceitos: JPG, PNG, GIF. Tamanho máximo: 2MB.',
            'bio': 'Máximo 500 caracteres.',
            'receber_emails': 'Ativar para receber e-mails sobre campanhas e relatórios',
            'receber_sms': 'Ativar para receber SMS em situações urgentes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Limitar tamanho da bio
        self.fields['bio'].widget.attrs['maxlength'] = '500'
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            # Validar tamanho do arquivo (2MB)
            if foto.size > 2 * 1024 * 1024:
                raise forms.ValidationError("O arquivo deve ter no máximo 2MB.")
            
            # Validar tipo do arquivo
            if not foto.content_type.startswith('image/'):
                raise forms.ValidationError("Apenas arquivos de imagem são permitidos.")
        
        return foto


# ===== FORMULÁRIO DE PARÂMETROS =====

class ParametroForm(forms.ModelForm):
    """Formulário para configuração de parâmetros do sistema"""
    
    class Meta:
        model = Parametro
        fields = [
            'parametro', 'descricao', 'tipo', 'categoria',
            'valor_texto', 'valor_numero', 'valor_decimal', 
            'valor_booleano', 'valor_data', 'editavel', 'ativo'
        ]
        widgets = {
            'parametro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nome_parametro (sem espaços)'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do que este parâmetro controla'
            }),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: email, marketing, sistema'
            }),
            'valor_texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Valor em texto'
            }),
            'valor_numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Valor numérico inteiro'
            }),
            'valor_decimal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': 'Valor decimal'
            }),
            'valor_booleano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'valor_data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'editavel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'parametro': 'Nome do Parâmetro *',
            'descricao': 'Descrição *',
            'tipo': 'Tipo do Valor *',
            'categoria': 'Categoria',
            'valor_texto': 'Valor (Texto)',
            'valor_numero': 'Valor (Número)',
            'valor_decimal': 'Valor (Decimal)',
            'valor_booleano': 'Valor (Verdadeiro/Falso)',
            'valor_data': 'Valor (Data)',
            'editavel': 'Editável pela Interface?',
            'ativo': 'Parâmetro Ativo?',
        }
        help_texts = {
            'parametro': 'Nome único do parâmetro, use underscore ao invés de espaços',
            'tipo': 'Tipo do valor que será armazenado',
            'categoria': 'Categoria para organizar parâmetros similares',
            'editavel': 'Se desmarcado, não poderá ser editado pela interface',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar JavaScript para mostrar/esconder campos baseado no tipo
        self.fields['tipo'].widget.attrs['onchange'] = 'toggleParametroFields(this.value)'
        
        # Se editando, mostrar apenas o campo do tipo atual
        if self.instance.pk:
            tipo_atual = self.instance.tipo
            for campo in ['valor_texto', 'valor_numero', 'valor_decimal', 'valor_booleano', 'valor_data']:
                if not campo.endswith(tipo_atual) and tipo_atual not in ['url', 'email']:
                    self.fields[campo].widget.attrs['style'] = 'display: none;'
    
    def clean_parametro(self):
        parametro = self.cleaned_data.get('parametro')
        if parametro:
            # Converter para lowercase e remover espaços
            parametro = parametro.lower().replace(' ', '_')
            
            # Validar formato
            import re
            if not re.match(r'^[a-z0-9_]+$', parametro):
                raise forms.ValidationError(
                    "Nome do parâmetro deve conter apenas letras minúsculas, números e underscore."
                )
        
        return parametro
    
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        
        # Validar que pelo menos um valor foi preenchido baseado no tipo
        if tipo == 'texto' and not cleaned_data.get('valor_texto'):
            self.add_error('valor_texto', 'Este campo é obrigatório para tipo texto.')
        elif tipo == 'numero' and cleaned_data.get('valor_numero') is None:
            self.add_error('valor_numero', 'Este campo é obrigatório para tipo número.')
        elif tipo == 'decimal' and cleaned_data.get('valor_decimal') is None:
            self.add_error('valor_decimal', 'Este campo é obrigatório para tipo decimal.')
        elif tipo == 'data' and not cleaned_data.get('valor_data'):
            self.add_error('valor_data', 'Este campo é obrigatório para tipo data.')
        elif tipo in ['url', 'email'] and not cleaned_data.get('valor_texto'):
            self.add_error('valor_texto', f'Este campo é obrigatório para tipo {tipo}.')
        
        return cleaned_data


# ===== FORMULÁRIO SIMPLES PARA CONFIGURAÇÕES =====

class ConfiguracoesForm(forms.Form):
    """Formulário simplificado para configurações principais do sistema"""
    
    nome_sistema = forms.CharField(
        max_length=100,
        label="Nome do Sistema",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email_sistema = forms.EmailField(
        label="E-mail do Sistema",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefone_suporte = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone de Suporte",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-mask': '(00) 00000-0000'
        })
    )
    timezone = forms.ChoiceField(
        choices=[
            ('America/Sao_Paulo', 'São Paulo (GMT-3)'),
            ('America/New_York', 'Nova York (GMT-5)'),
            ('Europe/London', 'Londres (GMT+0)'),
        ],
        label="Fuso Horário",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    debug_mode = forms.BooleanField(
        required=False,
        label="Modo Debug Ativo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Carregar valores atuais dos parâmetros
        self.fields['nome_sistema'].initial = Parametro.get_valor('nome_sistema', 'Portal Margaretas')
        self.fields['email_sistema'].initial = Parametro.get_valor('email_sistema', '')
        self.fields['telefone_suporte'].initial = Parametro.get_valor('telefone_suporte', '')
        self.fields['timezone'].initial = Parametro.get_valor('timezone', 'America/Sao_Paulo')
        self.fields['debug_mode'].initial = Parametro.get_valor('debug_mode', False)
    
    def save(self):
        """Salva as configurações nos parâmetros"""
        Parametro.set_valor('nome_sistema', self.cleaned_data['nome_sistema'], 'texto', 'Nome do sistema')
        Parametro.set_valor('email_sistema', self.cleaned_data['email_sistema'], 'email', 'E-mail principal do sistema')
        Parametro.set_valor('telefone_suporte', self.cleaned_data['telefone_suporte'], 'texto', 'Telefone de suporte')
        Parametro.set_valor('timezone', self.cleaned_data['timezone'], 'texto', 'Fuso horário do sistema')
        Parametro.set_valor('debug_mode', self.cleaned_data['debug_mode'], 'booleano', 'Modo debug ativo')


# ===== WIDGET PERSONALIZADO PARA DATA =====

class CustomDateInput(forms.DateInput):
    """Widget personalizado para campos de data"""
    input_type = 'date'
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class CustomDateTimeInput(forms.DateTimeInput):
    """Widget personalizado para campos de data e hora"""
    input_type = 'datetime-local'
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


# ===== FORMULÁRIO BASE PARA OUTROS FORMULÁRIOS =====

class BaseModelForm(forms.ModelForm):
    """Classe base para outros formulários com configurações padrão"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar classes Bootstrap automaticamente
        for field_name, field in self.fields.items():
            widget = field.widget
            
            if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.URLInput, 
                                 forms.NumberInput, forms.PasswordInput)):
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.DateInput, forms.DateTimeInput)):
                widget.attrs['class'] = 'form-control'
            elif isinstance(widget, forms.FileInput):
                widget.attrs['class'] = 'form-control'
            
            # Adicionar placeholder se não existir
            if hasattr(widget, 'attrs') and 'placeholder' not in widget.attrs:
                if isinstance(widget, (forms.TextInput, forms.EmailInput, forms.URLInput)):
                    widget.attrs['placeholder'] = f'Digite {field.label.lower()}...'


# ===== MIXIN PARA FORMULÁRIOS COM UPLOAD =====

class UploadMixin:
    """Mixin para formulários que precisam de upload de arquivos"""
    
    def clean_arquivo(self, field_name='arquivo', max_size=5*1024*1024, allowed_types=None):
        """
        Validação genérica para campos de upload
        
        Args:
            field_name: nome do campo de arquivo
            max_size: tamanho máximo em bytes (padrão: 5MB)
            allowed_types: lista de tipos MIME permitidos
        """
        arquivo = self.cleaned_data.get(field_name)
        
        if not arquivo:
            return arquivo
        
        # Validar tamanho
        if arquivo.size > max_size:
            size_mb = max_size / (1024 * 1024)
            raise forms.ValidationError(f"O arquivo deve ter no máximo {size_mb:.1f}MB.")
        
        # Validar tipo se especificado
        if allowed_types and arquivo.content_type not in allowed_types:
            tipos_str = ', '.join(allowed_types)
            raise forms.ValidationError(f"Tipos permitidos: {tipos_str}")
        
        return arquivo