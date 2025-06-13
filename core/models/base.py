# core/models/base.py

import logging
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

logger = logging.getLogger(__name__)


class Usuario(AbstractUser):
    """Modelo de usuário personalizado para o sistema"""
    
    NIVEL_CHOICES = [
        ('admin', 'Admin'),
        ('gestor', 'Gestor'),
        ('operador', 'Operador'),
        ('cliente', 'Cliente'),
    ]

    # Desabilitar relacionamentos padrão do Django
    groups = None
    user_permissions = None
    
    # Campos customizados
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='operador')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    
    # Campos herdados importantes
    is_superuser = models.BooleanField(default=False)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def nome_completo(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PerfilUsuario(models.Model):
    """Perfil estendido do usuário com informações adicionais"""
    
    NIVEL_CHOICES = [
        ('admin', 'Administrador'),
        ('gestor', 'Gestor'),
        ('operador', 'Operador'),
        ('cliente', 'Cliente'),
    ]
    
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='perfil',
        verbose_name="Usuário"
    )
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='operador',
        verbose_name="Nível de Acesso"
    )
    
    # Campos adicionais para o perfil
    foto = models.ImageField(
        upload_to='perfis/',
        blank=True,
        null=True,
        verbose_name="Foto do Perfil"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Biografia",
        help_text="Breve descrição sobre o usuário"
    )
    data_nascimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Nascimento"
    )
    
    # Configurações de notificação
    receber_emails = models.BooleanField(
        default=True,
        verbose_name="Receber E-mails"
    )
    receber_sms = models.BooleanField(
        default=False,
        verbose_name="Receber SMS"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        return f"Perfil de {self.usuario.nome_completo} - {self.get_nivel_display()}"
    
    class Meta:
        db_table = 'perfis_usuario'
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'


class Parametro(models.Model):
    """Modelo para armazenar parâmetros de configuração do sistema"""
    
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('numero', 'Número'),
        ('decimal', 'Decimal'),
        ('booleano', 'Verdadeiro/Falso'),
        ('data', 'Data'),
        ('url', 'URL'),
        ('email', 'E-mail'),
    ]
    
    # Identificação
    parametro = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="Nome do Parâmetro",
        help_text="Nome único do parâmetro (ex: smtp_servidor, taxa_conversao)"
    )
    descricao = models.CharField(
        max_length=200,
        verbose_name="Descrição",
        help_text="Descrição do que este parâmetro controla"
    )
    
    # Tipo e valor
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='texto',
        verbose_name="Tipo do Valor"
    )
    valor_texto = models.TextField(
        blank=True,
        null=True,
        verbose_name="Valor (Texto)"
    )
    valor_numero = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Valor (Número)"
    )
    valor_decimal = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        blank=True,
        null=True,
        verbose_name="Valor (Decimal)"
    )
    valor_booleano = models.BooleanField(
        default=False,
        verbose_name="Valor (Verdadeiro/Falso)"
    )
    valor_data = models.DateField(
        blank=True,
        null=True,
        verbose_name="Valor (Data)"
    )
    
    # Configurações
    categoria = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Categoria",
        help_text="Categoria para organizar parâmetros (ex: email, marketing, sistema)"
    )
    editavel = models.BooleanField(
        default=True,
        verbose_name="Editável",
        help_text="Se False, não pode ser alterado pela interface"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Criado por"
    )
    
    @property
    def valor(self):
        """Retorna o valor do parâmetro baseado no tipo"""
        if self.tipo == 'texto':
            return self.valor_texto
        elif self.tipo == 'numero':
            return self.valor_numero
        elif self.tipo == 'decimal':
            return float(self.valor_decimal) if self.valor_decimal else None
        elif self.tipo == 'booleano':
            return self.valor_booleano
        elif self.tipo == 'data':
            return self.valor_data
        elif self.tipo in ['url', 'email']:
            return self.valor_texto
        return None
    
    def set_valor(self, valor):
        """Define o valor do parâmetro baseado no tipo"""
        if self.tipo == 'texto' or self.tipo in ['url', 'email']:
            self.valor_texto = str(valor) if valor is not None else None
        elif self.tipo == 'numero':
            self.valor_numero = int(valor) if valor is not None else None
        elif self.tipo == 'decimal':
            self.valor_decimal = float(valor) if valor is not None else None
        elif self.tipo == 'booleano':
            self.valor_booleano = bool(valor)
        elif self.tipo == 'data':
            self.valor_data = valor
    
    @classmethod
    def get_valor(cls, parametro, default=None):
        """Método utilitário para buscar valor de um parâmetro"""
        try:
            param = cls.objects.get(parametro=parametro, ativo=True)
            return param.valor
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_valor(cls, parametro, valor, tipo='texto', descricao='', categoria=''):
        """Método utilitário para definir valor de um parâmetro"""
        param, created = cls.objects.get_or_create(
            parametro=parametro,
            defaults={
                'tipo': tipo,
                'descricao': descricao,
                'categoria': categoria,
            }
        )
        param.set_valor(valor)
        param.save()
        return param
    
    def __str__(self):
        return f"{self.parametro} = {self.valor}"
    
    class Meta:
        db_table = 'parametros'
        verbose_name = 'Parâmetro'
        verbose_name_plural = 'Parâmetros'
        ordering = ['categoria', 'parametro']


# ===== MODELO ABSTRATO PARA TIMESTAMPS =====

class TimeStampedModel(models.Model):
    """Modelo abstrato para adicionar timestamps a outros modelos"""
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        abstract = True


# ===== MODELO ABSTRATO PARA AUDITORIA =====

class AuditedModel(TimeStampedModel):
    """Modelo abstrato para auditoria completa (timestamps + usuário)"""
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name="Criado por"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name="Atualizado por"
    )
    
    class Meta:
        abstract = True


# ===== SIGNALS PARA CRIAR PERFIL AUTOMATICAMENTE =====

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Usuario)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """Cria perfil automaticamente quando usuário é criado"""
    if created:
        PerfilUsuario.objects.create(
            usuario=instance,
            nivel=instance.nivel,
            telefone=instance.telefone
        )
        logger.info(f"Perfil criado automaticamente para usuário {instance.username}")

@receiver(post_save, sender=Usuario)
def salvar_perfil_usuario(sender, instance, **kwargs):
    """Atualiza perfil quando usuário é salvo"""
    if hasattr(instance, 'perfil'):
        # Sincronizar dados do usuário com o perfil
        instance.perfil.nivel = instance.nivel
        instance.perfil.telefone = instance.telefone
        instance.perfil.save()