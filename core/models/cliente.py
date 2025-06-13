# core/models/cliente.py

from django.db import models
from django.conf import settings  # ← MUDANÇA 1: Trocar User por settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Cliente(models.Model):
    """Modelo para cadastro completo de clientes"""
    
    # Identificação única
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # === INFORMAÇÕES BÁSICAS DA EMPRESA ===
    nome_empresa = models.CharField(max_length=200, verbose_name="Nome da Empresa/Marca")
    cnpj_cpf = models.CharField(max_length=18, verbose_name="CNPJ/CPF", blank=True, null=True)
    endereco_completo = models.TextField(verbose_name="Endereço Completo", blank=True, null=True)
    
    # === HISTÓRIA E CONTEXTO ===
    historia_empresa = models.TextField(verbose_name="História da Empresa", blank=True, null=True)
    missao = models.TextField(verbose_name="Missão", blank=True, null=True)
    visao = models.TextField(verbose_name="Visão", blank=True, null=True)
    valores = models.TextField(verbose_name="Valores", blank=True, null=True)
    lista_produtos_servicos = models.TextField(verbose_name="Produtos ou Serviços")  # ← MUDANÇA 2: Renomeado
    
    # === RESPONSÁVEIS E CONTATOS ===
    responsavel_contrato = models.CharField(max_length=200, verbose_name="Responsável pelo Contrato")
    cargo_responsavel = models.CharField(max_length=100, verbose_name="Cargo do Responsável")
    contato_responsavel = models.CharField(max_length=100, verbose_name="Contato do Responsável")
    pessoa_contato_tecnico = models.CharField(max_length=200, verbose_name="Pessoa de Contato Técnico", blank=True, null=True)
    contato_tecnico = models.CharField(max_length=100, verbose_name="Contato Técnico", blank=True, null=True)
    
    # === INFORMAÇÕES FINANCEIRAS ===
    faturamento_anual = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Faturamento Anual Estimado", blank=True, null=True)
    
    # === PÚBLICO-ALVO ===
    descricao_publico = models.TextField(verbose_name="Descrição do Público-Alvo")
    necessidades_desejos = models.TextField(verbose_name="Necessidades e Desejos do Público")
    comportamento_compra = models.TextField(verbose_name="Comportamento de Compra")
    consideracoes_demograficas = models.TextField(verbose_name="Considerações Demográficas", blank=True, null=True)
    niveis_consciencia = models.TextField(verbose_name="Níveis de Consciência", blank=True, null=True)
    objecoes_comuns = models.TextField(verbose_name="Objeções Comuns", blank=True, null=True)
    tentativas_passadas = models.TextField(verbose_name="Tentativas Passadas que Não Funcionaram", blank=True, null=True)
    
    # === POSICIONAMENTO DA MARCA ===
    posicionamento_atual = models.TextField(verbose_name="Posicionamento Atual")
    objetivos_posicionamento = models.TextField(verbose_name="Objetivos de Posicionamento")
    diferenciacao = models.TextField(verbose_name="Diferenciação vs Concorrência", blank=True, null=True)
    
    # === COMUNICAÇÃO ===
    tom_voz = models.TextField(verbose_name="Tom de Voz da Marca")
    mensagem_principal = models.TextField(verbose_name="Mensagem Principal")
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
    
    canais_comunicacao = models.TextField(verbose_name="Canais de Comunicação e Perfis")
    
    # === OBJETIVOS ===
    objetivos_marketing = models.TextField(verbose_name="Objetivos de Marketing")
    metas_especificas = models.TextField(verbose_name="Metas Específicas")
    kpis_empresa = models.TextField(verbose_name="KPIs da Empresa")
    
    # === CONCORRÊNCIA ===
    analise_concorrencia = models.TextField(verbose_name="Análise da Concorrência")
    pontos_fortes_fracos_concorrencia = models.TextField(verbose_name="Pontos Fortes e Fracos da Concorrência")
    
    # === RECURSOS ===
    orcamento_marketing = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Orçamento Marketing", blank=True, null=True)
    equipe_marketing = models.TextField(verbose_name="Equipe de Marketing")
    recursos_tecnologicos = models.TextField(verbose_name="Recursos Tecnológicos")
    
    # === EXPECTATIVAS ===
    expectativas_agencia = models.TextField(verbose_name="Expectativas da Agência")
    resultados_esperados = models.TextField(verbose_name="Resultados Esperados")
    experiencia_agencias = models.TextField(verbose_name="Experiência com Agências de Tráfego", blank=True, null=True)
    criativos_performaram = models.TextField(verbose_name="Criativos que Performaram Melhor", blank=True, null=True)
    analise_campanhas_anteriores = models.TextField(verbose_name="O que Funcionou/Não Funcionou", blank=True, null=True)
    
    # === INFORMAÇÕES DIGITAIS ===
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Criado por")  # ← MUDANÇA 3
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nome_empresa


class ProdutoServicoEvento(models.Model):
    """Modelo para produtos, serviços, cursos e eventos específicos"""
    
    TIPO_CHOICES = [
        ('produto', 'Produto'),
        ('servico', 'Serviço'),
        ('curso', 'Curso'),
        ('evento', 'Evento'),
    ]
    
    FORMATO_CHOICES = [
        ('online', 'Online'),
        ('presencial', 'Presencial'),
        ('hibrido', 'Híbrido'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        related_name='produtos_servicos_relacionados'  # ← MUDANÇA 4: Novo related_name
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo")
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto/Serviço/Curso/Evento")
    descricao = models.TextField(verbose_name="Descrição")
    caracteristicas_beneficios = models.TextField(verbose_name="Características e Benefícios")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço", blank=True, null=True)
    posicionamento_mercado = models.TextField(verbose_name="Posicionamento no Mercado")
    
    # === MARKETING ===
    mensagens_marketing = models.TextField(verbose_name="Mensagens de Marketing")
    cronograma_lancamento = models.TextField(verbose_name="Cronograma de Lançamento")
    pacotes_opcoes = models.TextField(verbose_name="Pacotes e Opções", blank=True, null=True)
    objetivos_venda = models.TextField(verbose_name="Objetivos de Venda")
    metas_especificas = models.TextField(verbose_name="Metas Específicas")
    
    # === ESPECÍFICO PARA CURSOS E EVENTOS ===
    formato = models.CharField(max_length=20, choices=FORMATO_CHOICES, verbose_name="Formato", blank=True, null=True)
    duracao_agenda = models.TextField(verbose_name="Duração e Agenda", blank=True, null=True)
    palestrantes_instrutores = models.TextField(verbose_name="Palestrantes e Instrutores", blank=True, null=True)
    materiais_recursos = models.TextField(verbose_name="Materiais e Recursos", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Produto/Serviço/Evento"
        verbose_name_plural = "Produtos/Serviços/Eventos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"


class Campanha(models.Model):
    """Modelo para campanhas de marketing"""
    
    STATUS_CHOICES = [
        ('planejamento', 'Planejamento'),
        ('aprovacao', 'Aprovação'),
        ('ativa', 'Ativa'),
        ('pausada', 'Pausada'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]
    
    CANAIS_CHOICES = [
        ('google_search', 'Google Ads - Search'),
        ('google_display', 'Google Ads - Display'),
        ('google_youtube', 'Google Ads - YouTube'),
        ('facebook_ads', 'Facebook Ads'),
        ('instagram_ads', 'Instagram Ads'),
        ('tiktok_ads', 'TikTok Ads'),
        ('pinterest_ads', 'Pinterest Ads'),
        ('linkedin_ads', 'LinkedIn Ads'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='campanhas')
    produto_servico = models.ForeignKey(ProdutoServicoEvento, on_delete=models.SET_NULL, null=True, blank=True, related_name='campanhas')
    
    # === IDENTIFICAÇÃO ===
    nome_campanha = models.CharField(max_length=200, verbose_name="Nome da Campanha")
    descricao = models.TextField(verbose_name="Descrição da Campanha", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento', verbose_name="Status")
    
    # === OBJETIVOS ===
    objetivo_principal = models.TextField(verbose_name="Objetivo Principal")
    kpis_campanha = models.TextField(verbose_name="KPIs da Campanha")
    
    # Objetivos de Marketing (múltipla escolha)
    objetivos_marketing = models.JSONField(default=list, verbose_name="Objetivos de Marketing")
    
    # === PÚBLICO-ALVO ===
    publico_alvo = models.TextField(verbose_name="Público-Alvo da Campanha")
    idade_publico = models.CharField(max_length=50, verbose_name="Idade", blank=True, null=True)
    genero_publico = models.CharField(max_length=50, verbose_name="Gênero", blank=True, null=True)
    interesses_publico = models.TextField(verbose_name="Interesses", blank=True, null=True)
    comportamentos_publico = models.TextField(verbose_name="Comportamentos", blank=True, null=True)
    necessidades_desejos_publico = models.TextField(verbose_name="Necessidades e Desejos", blank=True, null=True)
    
    # === MENSAGEM E POSICIONAMENTO ===
    mensagem_topo_funil = models.TextField(verbose_name="Mensagem Topo de Funil", blank=True, null=True)
    mensagem_meio_funil = models.TextField(verbose_name="Mensagem Meio de Funil", blank=True, null=True)
    mensagem_fundo_funil = models.TextField(verbose_name="Mensagem Fundo de Funil", blank=True, null=True)
    posicionamento_vs_concorrencia = models.TextField(verbose_name="Posicionamento vs Concorrência")
    estrutura_funil_definida = models.BooleanField(default=False, verbose_name="Estrutura de Funil Definida?")
    transformacao_desejada = models.TextField(verbose_name="Transformação Desejada pelo Cliente")
    sentimentos_decisao_compra = models.TextField(verbose_name="Sentimentos para Decisão de Compra")
    dor_unica_resolve = models.TextField(verbose_name="Dor Única que Resolve")
    
    # === POSICIONAMENTO DA CAMPANHA ===
    diferenciacao_campanha = models.TextField(verbose_name="Diferenciação")
    valor_unico = models.TextField(verbose_name="Valor Único")
    promocao_preco = models.TextField(verbose_name="Promoção/Preço", blank=True, null=True)
    tom_voz_campanha = models.TextField(verbose_name="Tom e Voz da Campanha")
    
    # === ORÇAMENTO E CRONOGRAMA ===
    orcamento_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Orçamento Total")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_termino = models.DateField(verbose_name="Data de Término")
    duracao_dias = models.PositiveIntegerField(verbose_name="Duração em Dias", blank=True, null=True)
    
    # === CANAIS ===
    canais_utilizados = models.JSONField(default=list, verbose_name="Canais Utilizados")
    especificidades_canais = models.TextField(verbose_name="Especificidades de Cada Canal", blank=True, null=True)
    
    # === METAS ===
    metas_conversao = models.TextField(verbose_name="Metas de Conversão")
    metodo_medicao_conversao = models.TextField(verbose_name="Método de Medição de Conversão")
    meta_visitas_site = models.CharField(max_length=100, verbose_name="Meta de Visitas ao Site", blank=True, null=True)
    meta_leads_mes = models.IntegerField(verbose_name="Meta de Leads por Mês", blank=True, null=True)
    meta_aumento_vendas = models.CharField(max_length=100, verbose_name="Meta de Aumento de Vendas", blank=True, null=True)
    
    # === KPIs ESPECÍFICOS ===
    ctr_esperado = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="CTR Esperado (%)", blank=True, null=True)
    cpc_maximo = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="CPC Máximo", blank=True, null=True)
    cpa_maximo = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="CPA Máximo", blank=True, null=True)
    cac_maximo = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="CAC Máximo", blank=True, null=True)
    ltv_esperado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="LTV Esperado", blank=True, null=True)
    roas_minimo = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="ROAS Mínimo", blank=True, null=True)
    roi_esperado = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="ROI Esperado (%)", blank=True, null=True)
    
    # === REQUISITOS TÉCNICOS ===
    requisitos_tecnicos = models.TextField(verbose_name="Requisitos Técnicos", blank=True, null=True)
    especificacoes_anuncios = models.TextField(verbose_name="Especificações dos Anúncios", blank=True, null=True)
    
    # === CONFIGURAÇÃO TÉCNICA ===
    utms_personalizadas = models.TextField(verbose_name="UTMs Personalizadas", blank=True, null=True)
    landing_page_url = models.URLField(verbose_name="URL da Landing Page", blank=True, null=True)
    formularios_configurados = models.BooleanField(default=False, verbose_name="Formulários Configurados?")
    whatsapp_business_integrado = models.BooleanField(default=False, verbose_name="WhatsApp Business Integrado?")
    
    # === MONITORAMENTO ===
    FREQUENCIA_MONITORAMENTO_CHOICES = [
        ('diario', 'Diário'),
        ('semanal', 'Semanal'),
        ('mensal', 'Mensal'),
    ]
    
    frequencia_monitoramento = models.CharField(
        max_length=20, 
        choices=FREQUENCIA_MONITORAMENTO_CHOICES, 
        verbose_name="Frequência de Monitoramento"
    )
    estrategias_otimizacao = models.TextField(verbose_name="Estratégias de Otimização")
    
    # === CONTEXTO ESTRATÉGICO ===
    campanhas_concorrentes_benchmark = models.TextField(verbose_name="Campanhas Concorrentes (Benchmark)", blank=True, null=True)
    restricoes_legais = models.TextField(verbose_name="Restrições Legais/Compliance", blank=True, null=True)
    aprovacoes_necessarias = models.TextField(verbose_name="Aprovações Necessárias", blank=True, null=True)
    
    # === DADOS HISTÓRICOS ===
    campanhas_anteriores_empresa = models.TextField(verbose_name="Campanhas Anteriores da Empresa", blank=True, null=True)
    ticket_medio_atual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ticket Médio Atual", blank=True, null=True)
    ticket_medio_desejado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ticket Médio Desejado", blank=True, null=True)
    tempo_ciclo_venda = models.CharField(max_length=100, verbose_name="Tempo Médio do Ciclo de Venda", blank=True, null=True)
    
    # === METADADOS ===
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Criado por")  # ← MUDANÇA 5
    
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