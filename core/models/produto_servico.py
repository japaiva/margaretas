# core/models/produto_servico.py

import uuid
from django.db import models
from django.conf import settings

class ProdutoServicoEvento(models.Model):
    """Modelo para Produtos, Serviços e Eventos do cliente"""
    
    TIPO_CHOICES = [
        ('produto', 'Produto'),
        ('servico', 'Serviço'),
        ('curso', 'Curso'),
        ('evento', 'Evento'),
    ]
    
    # Identificação
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='produtos_servicos')
    
    # Informações Básicas
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto/Serviço/Curso/Evento")
    descricao = models.TextField(verbose_name="Descrição", blank=True, null=True)
    
    # Características e Benefícios
    caracteristicas_beneficios = models.TextField(
        verbose_name="Características e Benefícios", 
        blank=True, 
        null=True
    )
    
    # Preço e Posicionamento
    preco = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Preço (R$)", 
        blank=True, 
        null=True
    )
    posicionamento_mercado = models.TextField(
        verbose_name="Posicionamento no Mercado", 
        blank=True, 
        null=True
    )
    
    # Marketing
    mensagens_materiais_marketing = models.TextField(
        verbose_name="Mensagens e Materiais de Marketing", 
        blank=True, 
        null=True,
        help_text="Quais mensagens e materiais serão usados para promover?"
    )
    
    # Cronograma
    data_lancamento = models.DateField(
        verbose_name="Data de Lançamento", 
        blank=True, 
        null=True
    )
    cronograma_producao = models.TextField(
        verbose_name="Cronograma para Produção e Distribuição", 
        blank=True, 
        null=True
    )
    
    # Pacotes e Opções
    pacotes_opcoes = models.TextField(
        verbose_name="Pacotes e Opções de Serviço", 
        blank=True, 
        null=True,
        help_text="Quais pacotes e opções serão oferecidos?"
    )
    
    # Objetivos e Metas
    objetivos_venda = models.TextField(
        verbose_name="Objetivos da Venda", 
        blank=True, 
        null=True,
        help_text="Ex: gerar inscrições, aumentar receita"
    )
    metas_especificas = models.TextField(
        verbose_name="Metas Específicas", 
        blank=True, 
        null=True,
        help_text="Ex: número de inscrições, receita esperada"
    )
    
    # Campos específicos para Cursos e Eventos
    formato = models.CharField(
        max_length=100, 
        verbose_name="Formato", 
        blank=True, 
        null=True,
        help_text="Online, presencial, híbrido"
    )
    duracao = models.CharField(
        max_length=100, 
        verbose_name="Duração", 
        blank=True, 
        null=True
    )
    agenda = models.TextField(
        verbose_name="Agenda/Programação", 
        blank=True, 
        null=True
    )
    palestrantes_instrutores = models.TextField(
        verbose_name="Palestrantes e Instrutores", 
        blank=True, 
        null=True
    )
    materiais_recursos = models.TextField(
        verbose_name="Materiais e Recursos", 
        blank=True, 
        null=True,
        help_text="Materiais fornecidos aos participantes"
    )
    
    # Status
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name="Criado por"
    )
    
    class Meta:
        verbose_name = "Produto/Serviço/Evento"
        verbose_name_plural = "Produtos/Serviços/Eventos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.nome}"
    
    @property
    def completude_percentual(self):
        """Calcula percentual de completude das informações"""
        campos_importantes = [
            'nome', 'descricao', 'caracteristicas_beneficios', 
            'preco', 'posicionamento_mercado', 'objetivos_venda'
        ]
        
        campos_preenchidos = sum(
            1 for campo in campos_importantes 
            if getattr(self, campo) and str(getattr(self, campo)).strip()
        )
        
        return (campos_preenchidos / len(campos_importantes)) * 100