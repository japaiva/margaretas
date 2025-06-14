# core/models/cliente.py - VERSÃO REFATORADA

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Cliente(models.Model):
    """Modelo simplificado para cadastro de clientes"""
    
    # Identificação única
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # === INFORMAÇÕES BÁSICAS DA EMPRESA (FORM SIMPLES) ===
    nome_empresa = models.CharField(max_length=200, verbose_name="Nome da Empresa/Marca")
    cnpj_cpf = models.CharField(max_length=18, verbose_name="CNPJ/CPF", blank=True, null=True)
    endereco_completo = models.TextField(verbose_name="Endereço Completo", blank=True, null=True)
    
    # === HISTÓRICO E CONTEXTO ===
    historia_empresa = models.TextField(verbose_name="História da Empresa", blank=True, null=True)
    missao = models.TextField(verbose_name="Missão", blank=True, null=True)
    visao = models.TextField(verbose_name="Visão", blank=True, null=True)
    valores = models.TextField(verbose_name="Valores", blank=True, null=True)
    lista_produtos_servicos = models.TextField(verbose_name="Produtos ou Serviços", blank=True, null=True)
    
    # === RESPONSÁVEIS E CONTATOS ===
    responsavel_contrato = models.CharField(max_length=200, verbose_name="Responsável pelo Contrato", blank=True, null=True)
    cargo_responsavel = models.CharField(max_length=100, verbose_name="Cargo do Responsável", blank=True, null=True)
    contato_responsavel = models.CharField(max_length=100, verbose_name="Contato do Responsável", blank=True, null=True)
    pessoa_contato_tecnico = models.CharField(max_length=200, verbose_name="Pessoa de Contato Técnico", blank=True, null=True)
    contato_tecnico = models.CharField(max_length=100, verbose_name="Contato Técnico", blank=True, null=True)
    
    # === INFORMAÇÕES FINANCEIRAS ===
    faturamento_anual = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Faturamento Anual Estimado", blank=True, null=True)
    
    # === PÚBLICO-ALVO (WIZARD STEP 1) ===
    descricao_publico = models.TextField(verbose_name="Descrição do Público-Alvo", blank=True, null=True)
    necessidades_desejos = models.TextField(verbose_name="Necessidades e Desejos do Público", blank=True, null=True)
    comportamento_compra = models.TextField(verbose_name="Comportamento de Compra", blank=True, null=True)
    consideracoes_demograficas = models.TextField(verbose_name="Considerações Demográficas", blank=True, null=True)
    niveis_consciencia = models.TextField(verbose_name="Níveis de Consciência", blank=True, null=True)
    objecoes_comuns = models.TextField(verbose_name="Objeções Comuns", blank=True, null=True)
    tentativas_passadas = models.TextField(verbose_name="Tentativas Passadas que Não Funcionaram", blank=True, null=True)
    
    # === POSICIONAMENTO E COMUNICAÇÃO (WIZARD STEP 2) ===
    posicionamento_atual = models.TextField(verbose_name="Posicionamento Atual", blank=True, null=True)
    objetivos_posicionamento = models.TextField(verbose_name="Objetivos de Posicionamento", blank=True, null=True)
    diferenciacao = models.TextField(verbose_name="Diferenciação vs Concorrência", blank=True, null=True)
    tom_voz = models.TextField(verbose_name="Tom de Voz da Marca", blank=True, null=True)
    mensagem_principal = models.TextField(verbose_name="Mensagem Principal", blank=True, null=True)
    manual_marca = models.BooleanField(default=False, verbose_name="Possui Manual de Marca?")
    manifesto_marca = models.TextField(verbose_name="Manifesto da Marca", blank=True, null=True)
    
    # === ARQUÉTIPOS (Múltipla Escolha) ===
    ARQUETIPOS_CHOICES = [
        ('mestre_sabio', 'Um mestre sábio'),
        ('rebelde_provocador', 'Um rebelde provocador'),
        ('cuidador_acolhedor', 'Um cuidador acolhedor'),
        ('heroi_determinado', 'Um herói determinado'),
        ('artista_criativo', 'Um artista criativo'),
        ('explorador_curioso', 'Um explorador curioso'),
    ]
    arquetipos = models.JSONField(default=list, verbose_name="Arquétipos da Marca", blank=True)
    canais_comunicacao = models.TextField(verbose_name="Canais de Comunicação e Perfis", blank=True, null=True)
    
    # === OBJETIVOS E ESTRATÉGIA (WIZARD STEP 3) ===
    objetivos_marketing = models.TextField(verbose_name="Objetivos de Marketing", blank=True, null=True)
    metas_especificas = models.TextField(verbose_name="Metas Específicas", blank=True, null=True)
    kpis_empresa = models.TextField(verbose_name="KPIs da Empresa", blank=True, null=True)
    analise_concorrencia = models.TextField(verbose_name="Análise da Concorrência", blank=True, null=True)
    pontos_fortes_fracos_concorrencia = models.TextField(verbose_name="Pontos Fortes e Fracos da Concorrência", blank=True, null=True)
    
    # === RECURSOS E EXPECTATIVAS (WIZARD STEP 4) ===
    orcamento_marketing = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Orçamento Marketing", blank=True, null=True)
    equipe_marketing = models.TextField(verbose_name="Equipe de Marketing", blank=True, null=True)
    recursos_tecnologicos = models.TextField(verbose_name="Recursos Tecnológicos", blank=True, null=True)
    expectativas_agencia = models.TextField(verbose_name="Expectativas da Agência", blank=True, null=True)
    resultados_esperados = models.TextField(verbose_name="Resultados Esperados", blank=True, null=True)
    experiencia_agencias = models.TextField(verbose_name="Experiência com Agências de Tráfego", blank=True, null=True)
    criativos_performaram = models.TextField(verbose_name="Criativos que Performaram Melhor", blank=True, null=True)
    analise_campanhas_anteriores = models.TextField(verbose_name="O que Funcionou/Não Funcionou", blank=True, null=True)
    
    # === INFORMAÇÕES DIGITAIS BÁSICAS ===
    website_principal = models.URLField(verbose_name="Website Principal", blank=True, null=True)
    outros_dominios = models.TextField(verbose_name="Outros Domínios", blank=True, null=True)
    google_analytics = models.BooleanField(default=False, verbose_name="Google Analytics Configurado?")
    tag_manager = models.BooleanField(default=False, verbose_name="Tag Manager Configurado?")
    pixel_facebook = models.BooleanField(default=False, verbose_name="Pixel Facebook Instalado?")
    crm_utilizado = models.CharField(max_length=100, verbose_name="CRM Utilizado", blank=True, null=True)
    
    # === CONTEXTO ADICIONAL ===
    principais_desafios = models.TextField(verbose_name="Principais Desafios do Mercado", blank=True, null=True)
    sazonalidades = models.TextField(verbose_name="Sazonalidades do Negócio", blank=True, null=True)
    certificacoes_diferenciais = models.TextField(verbose_name="Certificações ou Diferenciais", blank=True, null=True)
    
    # === METADADOS ===
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Criado por")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    # === FLAGS DE COMPLETUDE ===
    briefing_completo = models.BooleanField(default=False, verbose_name="Briefing Estratégico Completo?")
    data_briefing = models.DateTimeField(null=True, blank=True, verbose_name="Data de Conclusão do Briefing")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome_empresa

    @property
    def briefing_progress(self):
        """Calcula o progresso do briefing (0-100%)"""
        steps = [
            # Step 1: Público-Alvo
            bool(self.descricao_publico and self.necessidades_desejos and self.comportamento_compra),
            # Step 2: Posicionamento
            bool(self.posicionamento_atual and self.objetivos_posicionamento and self.tom_voz and self.mensagem_principal and self.canais_comunicacao),
            # Step 3: Objetivos
            bool(self.objetivos_marketing and self.metas_especificas and self.kpis_empresa and self.analise_concorrencia and self.pontos_fortes_fracos_concorrencia),
            # Step 4: Recursos
            bool(self.equipe_marketing and self.recursos_tecnologicos and self.expectativas_agencia and self.resultados_esperados)
        ]
        completed_steps = sum(steps)
        return (completed_steps / len(steps)) * 100


class ClienteChecklist(models.Model):
    """Checklist operacional para execução de campanhas"""
    
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name='checklist')
    
    # === REFERÊNCIAS E MATERIAIS ===
    banco_imagens_videos = models.BooleanField(default=False, verbose_name="Possui banco de imagens/vídeos?")
    responsavel_conteudo = models.CharField(max_length=200, verbose_name="Responsável por conteúdo", blank=True, null=True)
    acesso_criativos = models.BooleanField(default=False, verbose_name="Tem acesso a criativos utilizados?")
    pasta_materiais = models.URLField(verbose_name="Link da pasta de materiais", blank=True, null=True)
    
    # === PERMISSÕES E ACESSOS META ===
    liberacao_meta = models.BooleanField(default=False, verbose_name="Liberação Meta com cliente")
    business_manager_ativo = models.BooleanField(default=False, verbose_name="Business Manager ativo?")
    dominio_verificado = models.BooleanField(default=False, verbose_name="Domínio verificado?")
    pixel_instalado = models.BooleanField(default=False, verbose_name="Pixel instalado?")
    conversoes_api_ativas = models.BooleanField(default=False, verbose_name="Conversões API ativas?")
    acesso_conta_anuncios = models.BooleanField(default=False, verbose_name="Acesso à conta de anúncios?")
    
    # === GOOGLE ADS E FERRAMENTAS ===
    conta_google_ads = models.BooleanField(default=False, verbose_name="Conta no Google Ads?")
    search_console = models.BooleanField(default=False, verbose_name="Google Search Console configurado?")
    
    # === OBSERVAÇÕES ===
    observacoes = models.TextField(verbose_name="Observações", blank=True, null=True)
    
    # === METADADOS ===
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = "Checklist Operacional"
        verbose_name_plural = "Checklists Operacionais"
    
    @property
    def completude_percentual(self):
        """Calcula percentual de itens marcados"""
        campos_checklist = [
            'banco_imagens_videos', 'acesso_criativos', 'liberacao_meta',
            'business_manager_ativo', 'dominio_verificado', 'pixel_instalado',
            'conversoes_api_ativas', 'acesso_conta_anuncios', 'conta_google_ads',
            'search_console'
        ]
        
        total_campos = len(campos_checklist)
        campos_marcados = sum(1 for campo in campos_checklist if getattr(self, campo))
        
        return (campos_marcados / total_campos) * 100

class Campanha(models.Model):
    """Modelo simplificado para campanhas de marketing"""
    
    STATUS_CHOICES = [
        ('planejamento', 'Planejamento'),
        ('aprovacao', 'Aprovação'),
        ('ativa', 'Ativa'),
        ('pausada', 'Pausada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='campanhas')
    
    # === IDENTIFICAÇÃO ===
    nome_campanha = models.CharField(max_length=200, verbose_name="Nome da Campanha")
    descricao = models.TextField(verbose_name="Descrição da Campanha", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento', verbose_name="Status")
    
    # === OBJETIVOS ===
    objetivo_principal = models.TextField(verbose_name="Objetivo Principal")
    kpis_campanha = models.TextField(verbose_name="KPIs da Campanha")
    
    # === PÚBLICO-ALVO ===
    publico_alvo = models.TextField(verbose_name="Público-Alvo da Campanha")
    
    # === ORÇAMENTO E CRONOGRAMA ===
    orcamento_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Orçamento Total")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_termino = models.DateField(verbose_name="Data de Término")
    duracao_dias = models.PositiveIntegerField(verbose_name="Duração em Dias", blank=True, null=True)
    
    # === METADADOS ===
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Criado por")
    
    class Meta:
        verbose_name = "Campanha"
        verbose_name_plural = "Campanhas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nome_campanha} - {self.cliente.nome_empresa}"
    
    def save(self, *args, **kwargs):
        # Calcular duração automaticamente
        if self.data_inicio and self.data_termino:
            self.duracao_dias = (self.data_termino - self.data_inicio).days
        super().save(*args, **kwargs)