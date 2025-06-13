from django import forms
from django.forms import widgets
from core.models import Cliente, ProdutoServicoEvento, Campanha


class ClienteForm(forms.ModelForm):
    """Formulário para cadastro de clientes"""
    
    # Campos com múltipla escolha para arquétipos
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
        exclude = ['id', 'created_at', 'updated_at', 'created_by']
        
        widgets = {
            # Campos de texto longo
            'historia_empresa': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte a história da empresa, marcos importantes, evolução...'}),
            'missao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual é a missão da empresa?'}),
            'visao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual é a visão da empresa?'}),
            'valores': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais são os valores da empresa?'}),
            'produtos_servicos': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva os produtos ou serviços oferecidos'}),
            
            # Público-alvo
            'descricao_publico': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Idade, gênero, interesses, comportamentos...'}),
            'necessidades_desejos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que o público busca? Quais são suas dores?'}),
            'comportamento_compra': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como o público costuma comprar?'}),
            'consideracoes_demograficas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Onde está localizado? Onde quer atingir?'}),
            'niveis_consciencia': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Nível de conhecimento sobre o produto/serviço'}),
            'objecoes_comuns': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Preço, tempo, confiança, etc.'}),
            'tentativas_passadas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que já tentaram e não funcionou?'}),
            
            # Posicionamento
            'posicionamento_atual': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como a marca está posicionada hoje?'}),
            'objetivos_posicionamento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como querem ser percebidos?'}),
            'diferenciacao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que os diferencia da concorrência?'}),
            
            # Comunicação
            'tom_voz': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Formal, descontraído, técnico, amigável...'}),
            'mensagem_principal': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual mensagem principal querem transmitir?'}),
            'manifesto_marca': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Manifesto ou propósito da marca'}),
            'canais_comunicacao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Redes sociais, site, email... (inclua links/perfis)'}),
            
            # Objetivos
            'objetivos_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais são os objetivos de marketing?'}),
            'metas_especificas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Metas mensuráveis e específicas'}),
            'kpis_empresa': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como medem o sucesso?'}),
            
            # Concorrência
            'analise_concorrencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Principais concorrentes (incluir sites/perfis)'}),
            'pontos_fortes_fracos_concorrencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que fazem bem e onde falham?'}),
            
            # Recursos
            'equipe_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quem é a equipe responsável?'}),
            'recursos_tecnologicos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ferramentas e tecnologias disponíveis'}),
            
            # Expectativas
            'expectativas_agencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que esperam da parceria?'}),
            'resultados_esperados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Que resultados esperam?'}),
            'experiencia_agencias': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Já trabalharam com outras agências? Como foi?'}),
            'criativos_performaram': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais materiais funcionaram bem?'}),
            'analise_campanhas_anteriores': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que funcionou ou não funcionou?'}),
            
            # Contexto adicional
            'principais_desafios': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Principais desafios do mercado atual'}),
            'sazonalidades': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Períodos de alta/baixa, datas importantes'}),
            'certificacoes_diferenciais': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Certificações, prêmios, diferenciais técnicos'}),
            
            # Endereço
            'endereco_completo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Endereço completo da empresa'}),
            'outros_dominios': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Outros sites ou domínios da empresa'}),
            
            # Campos de checkbox
            'manual_marca': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'google_analytics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tag_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pixel_facebook': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Campos monetários
            'faturamento_anual': forms.NumberInput(attrs={'placeholder': 'Ex: 1000000.00', 'step': '0.01'}),
            'orcamento_marketing': forms.NumberInput(attrs={'placeholder': 'Ex: 50000.00', 'step': '0.01'}),
            
            # Campos de URL
            'website_principal': forms.URLInput(attrs={'placeholder': 'https://exemplo.com.br'}),
            
            # Campos de texto simples
            'nome_empresa': forms.TextInput(attrs={'placeholder': 'Nome da empresa ou marca'}),
            'cnpj_cpf': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00 ou 000.000.000-00'}),
            'responsavel_contrato': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'cargo_responsavel': forms.TextInput(attrs={'placeholder': 'Cargo na empresa'}),
            'contato_responsavel': forms.TextInput(attrs={'placeholder': 'Email ou telefone'}),
            'pessoa_contato_tecnico': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'contato_tecnico': forms.TextInput(attrs={'placeholder': 'Email ou telefone'}),
            'crm_utilizado': forms.TextInput(attrs={'placeholder': 'Ex: Pipedrive, Salesforce, RD Station'}),
        }
        
        labels = {
            'nome_empresa': 'Nome da Empresa/Marca *',
            'cnpj_cpf': 'CNPJ/CPF',
            'endereco_completo': 'Endereço Completo',
            'historia_empresa': 'História da Empresa',
            'missao': 'Missão da Empresa',
            'visao': 'Visão da Empresa',
            'valores': 'Valores da Empresa',
            'produtos_servicos': 'Produtos ou Serviços *',
            'responsavel_contrato': 'Responsável pelo Contrato *',
            'cargo_responsavel': 'Cargo do Responsável *',
            'contato_responsavel': 'Contato do Responsável *',
            'pessoa_contato_tecnico': 'Pessoa de Contato Técnico',
            'contato_tecnico': 'Contato da Pessoa Técnica',
            'faturamento_anual': 'Faturamento Anual Estimado (R$)',
            'descricao_publico': 'Descrição do Público-Alvo *',
            'necessidades_desejos': 'Necessidades e Desejos do Público *',
            'comportamento_compra': 'Comportamento de Compra *',
            'consideracoes_demograficas': 'Considerações Demográficas',
            'niveis_consciencia': 'Níveis de Consciência sobre o Serviço',
            'objecoes_comuns': 'Objeções ou Resistências Comuns',
            'tentativas_passadas': 'O que Já Tentaram e Não Funcionou',
            'posicionamento_atual': 'Posicionamento Atual *',
            'objetivos_posicionamento': 'Objetivos de Posicionamento *',
            'diferenciacao': 'Diferenciação vs Concorrência',
            'tom_voz': 'Tom e Voz da Marca *',
            'mensagem_principal': 'Mensagem Principal *',
            'manual_marca': 'Possui Manual de Marca?',
            'manifesto_marca': 'Manifesto da Marca',
            'canais_comunicacao': 'Canais de Comunicação e Perfis *',
            'objetivos_marketing': 'Objetivos de Marketing *',
            'metas_especificas': 'Metas Específicas *',
            'kpis_empresa': 'KPIs da Empresa *',
            'analise_concorrencia': 'Análise da Concorrência *',
            'pontos_fortes_fracos_concorrencia': 'Pontos Fortes e Fracos da Concorrência *',
            'orcamento_marketing': 'Orçamento de Marketing (R$)',
            'equipe_marketing': 'Equipe de Marketing *',
            'recursos_tecnologicos': 'Recursos Tecnológicos *',
            'expectativas_agencia': 'Expectativas da Agência *',
            'resultados_esperados': 'Resultados Esperados *',
            'experiencia_agencias': 'Experiência com Agências de Tráfego',
            'criativos_performaram': 'Criativos que Performaram Melhor',
            'analise_campanhas_anteriores': 'O que Funcionou/Não Funcionou',
            'website_principal': 'Website Principal',
            'outros_dominios': 'Outros Domínios',
            'google_analytics': 'Google Analytics Configurado?',
            'tag_manager': 'Google Tag Manager Configurado?',
            'pixel_facebook': 'Pixel do Facebook Instalado?',
            'crm_utilizado': 'CRM Utilizado',
            'principais_desafios': 'Principais Desafios do Mercado',
            'sazonalidades': 'Sazonalidades do Negócio',
            'certificacoes_diferenciais': 'Certificações ou Diferenciais',
            'ativo': 'Cliente Ativo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes CSS aos campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.URLInput, forms.NumberInput)):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
    
    def clean_arquetipos(self):
        arquetipos = self.cleaned_data.get('arquetipos', [])
        if len(arquetipos) > 3:
            raise forms.ValidationError("Selecione no máximo 3 arquétipos.")
        return arquetipos


class ProdutoServicoEventoForm(forms.ModelForm):
    """Formulário para produtos, serviços, cursos e eventos"""
    
    class Meta:
        model = ProdutoServicoEvento
        exclude = ['id', 'created_at', 'updated_at']
        
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto/serviço/curso/evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada'}),
            'caracteristicas_beneficios': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Principais características e benefícios'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 299.90'}),
            'posicionamento_mercado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Como está posicionado no mercado?'}),
            'mensagens_marketing': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mensagens e materiais de marketing'}),
            'cronograma_lancamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Data de lançamento, prazos, distribuição'}),
            'pacotes_opcoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diferentes pacotes ou opções oferecidas'}),
            'objetivos_venda': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Objetivos da venda (inscrições, receita, etc.)'}),
            'metas_especificas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Metas mensuráveis específicas'}),
            'formato': forms.Select(attrs={'class': 'form-select'}),
            'duracao_agenda': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Duração e agenda detalhada'}),
            'palestrantes_instrutores': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Quem são os palestrantes e instrutores'}),
            'materiais_recursos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Materiais fornecidos aos participantes'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'cliente': 'Cliente *',
            'tipo': 'Tipo *',
            'nome': 'Nome *',
            'descricao': 'Descrição *',
            'caracteristicas_beneficios': 'Características e Benefícios *',
            'preco': 'Preço (R$)',
            'posicionamento_mercado': 'Posicionamento no Mercado *',
            'mensagens_marketing': 'Mensagens de Marketing *',
            'cronograma_lancamento': 'Cronograma de Lançamento *',
            'pacotes_opcoes': 'Pacotes e Opções',
            'objetivos_venda': 'Objetivos de Venda *',
            'metas_especificas': 'Metas Específicas *',
            'formato': 'Formato (para cursos/eventos)',
            'duracao_agenda': 'Duração e Agenda',
            'palestrantes_instrutores': 'Palestrantes e Instrutores',
            'materiais_recursos': 'Materiais e Recursos',
            'ativo': 'Ativo?'
        }


class CampanhaForm(forms.ModelForm):
    """Formulário para campanhas"""
    
    # Campos com múltipla escolha
    OBJETIVOS_MARKETING_CHOICES = [
        ('aumentar_trafego', 'Aumentar o tráfego do site'),
        ('gerar_leads', 'Gerar leads'),
        ('aumentar_vendas', 'Aumentar as vendas'),
        ('melhorar_visibilidade', 'Melhorar a visibilidade da marca no longo prazo'),
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
    
    objetivos_marketing = forms.MultipleChoiceField(
        choices=OBJETIVOS_MARKETING_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Selecione todos os objetivos aplicáveis"
    )
    
    canais_utilizados = forms.MultipleChoiceField(
        choices=CANAIS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Selecione os canais que serão utilizados"
    )
    
    class Meta:
        model = Campanha
        exclude = ['id', 'created_at', 'updated_at', 'created_by', 'duracao_dias']
        
        widgets = {
            # Identificação
            'nome_campanha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da campanha'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da campanha'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            
            # Objetivos
            'objetivo_principal': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qual o objetivo principal?'}),
            'kpis_campanha': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'KPIs para medir sucesso'}),
            
            # Público-alvo
            'publico_alvo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição do público-alvo da campanha'}),
            'idade_publico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 25-45 anos'}),
            'genero_publico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Todos, Masculino, Feminino'}),
            'interesses_publico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Interesses específicos do público'}),
            'comportamentos_publico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comportamentos online e offline'}),
            'necessidades_desejos_publico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O que este público busca?'}),
            
            # Mensagens por funil
            'mensagem_topo_funil': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mensagem para quem não conhece o produto'}),
            'mensagem_meio_funil': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mensagem para quem está considerando'}),
            'mensagem_fundo_funil': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mensagem para quem está pronto para comprar'}),
            
            'posicionamento_vs_concorrencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Como se posicionar vs concorrência?'}),
            'estrutura_funil_definida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'transformacao_desejada': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Que transformação o cliente deseja viver?'}),
            'sentimentos_decisao_compra': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Que sentimentos ele precisa ter?'}),
            'dor_unica_resolve': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qual dor você resolve melhor que todos?'}),
            
            # Posicionamento da campanha
            'diferenciacao_campanha': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Diferenciação desta campanha'}),
            'valor_unico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Valor único oferecido'}),
            'promocao_preco': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Promoções ou preços especiais'}),
            'tom_voz_campanha': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tom de voz específico desta campanha'}),
            
            # Orçamento e cronograma
            'orcamento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 10000.00'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            'especificidades_canais': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Palavras-chave, públicos específicos, formatos por canal'}),
            
            # Metas
            'metas_conversao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Downloads, formulários, compras, etc.'}),
            'metodo_medicao_conversao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Pixels, códigos, ferramentas de tracking'}),
            'meta_visitas_site': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +50% ou 10.000 visitas/mês'}),
            'meta_leads_mes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 100'}),
            'meta_aumento_vendas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +30% ou R$ 50.000/mês'}),
            
            # KPIs específicos
            'ctr_esperado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 3.5'}),
            'cpc_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 2.50'}),
            'cpa_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 50.00'}),
            'cac_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 100.00'}),
            'ltv_esperado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 500.00'}),
            'roas_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 4.0'}),
            'roi_esperado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 300'}),
            
            # Requisitos técnicos
            'requisitos_tecnicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Integrações, cookies, ferramentas necessárias'}),
            'especificacoes_anuncios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tamanhos, formatos, resoluções'}),
            
            # Configuração técnica
            'utms_personalizadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'UTMs específicas para tracking'}),
            'landing_page_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://exemplo.com/landing-page'}),
            'formularios_configurados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'whatsapp_business_integrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Monitoramento
            'frequencia_monitoramento': forms.Select(attrs={'class': 'form-select'}),
            'estrategias_otimizacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ajustes de lances, anúncios, audiences'}),
            
            # Contexto estratégico
            'campanhas_concorrentes_benchmark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Campanhas que funcionaram bem para concorrentes'}),
            'restricoes_legais': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Compliance, restrições setoriais'}),
            'aprovacoes_necessarias': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Hierarquia de aprovação dos materiais'}),
            
            # Dados históricos
            'campanhas_anteriores_empresa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'O que funcionou/não funcionou antes'}),
            'ticket_medio_atual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 150.00'}),
            'ticket_medio_desejado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 200.00'}),
            'tempo_ciclo_venda': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 7 dias, 1 mês'}),
        }
        
        labels = {
            'cliente': 'Cliente *',
            'produto_servico': 'Produto/Serviço/Evento',
            'nome_campanha': 'Nome da Campanha *',
            'descricao': 'Descrição da Campanha',
            'status': 'Status *',
            'objetivo_principal': 'Objetivo Principal *',
            'kpis_campanha': 'KPIs da Campanha *',
            'publico_alvo': 'Público-Alvo da Campanha *',
            'idade_publico': 'Idade do Público',
            'genero_publico': 'Gênero do Público',
            'interesses_publico': 'Interesses',
            'comportamentos_publico': 'Comportamentos',
            'necessidades_desejos_publico': 'Necessidades e Desejos',
            'mensagem_topo_funil': 'Mensagem Topo de Funil',
            'mensagem_meio_funil': 'Mensagem Meio de Funil',
            'mensagem_fundo_funil': 'Mensagem Fundo de Funil',
            'posicionamento_vs_concorrencia': 'Posicionamento vs Concorrência *',
            'estrutura_funil_definida': 'Estrutura de Funil Já Definida?',
            'transformacao_desejada': 'Transformação Desejada pelo Cliente *',
            'sentimentos_decisao_compra': 'Sentimentos para Decisão de Compra *',
            'dor_unica_resolve': 'Dor Única que Resolve *',
            'diferenciacao_campanha': 'Diferenciação *',
            'valor_unico': 'Valor Único *',
            'promocao_preco': 'Promoção/Preço',
            'tom_voz_campanha': 'Tom e Voz da Campanha *',
            'orcamento_total': 'Orçamento Total (R$) *',
            'data_inicio': 'Data de Início *',
            'data_termino': 'Data de Término *',
            'especificidades_canais': 'Especificidades dos Canais',
            'metas_conversao': 'Metas de Conversão *',
            'metodo_medicao_conversao': 'Método de Medição de Conversão *',
            'meta_visitas_site': 'Meta de Visitas ao Site',
            'meta_leads_mes': 'Meta de Leads por Mês',
            'meta_aumento_vendas': 'Meta de Aumento de Vendas',
            'ctr_esperado': 'CTR Esperado (%)',
            'cpc_maximo': 'CPC Máximo (R$)',
            'cpa_maximo': 'CPA Máximo (R$)',
            'cac_maximo': 'CAC Máximo (R$)',
            'ltv_esperado': 'LTV Esperado (R$)',
            'roas_minimo': 'ROAS Mínimo',
            'roi_esperado': 'ROI Esperado (%)',
            'requisitos_tecnicos': 'Requisitos Técnicos',
            'especificacoes_anuncios': 'Especificações dos Anúncios',
            'utms_personalizadas': 'UTMs Personalizadas',
            'landing_page_url': 'URL da Landing Page',
            'formularios_configurados': 'Formulários Configurados?',
            'whatsapp_business_integrado': 'WhatsApp Business Integrado?',
            'frequencia_monitoramento': 'Frequência de Monitoramento *',
            'estrategias_otimizacao': 'Estratégias de Otimização *',
            'campanhas_concorrentes_benchmark': 'Campanhas Concorrentes (Benchmark)',
            'restricoes_legais': 'Restrições Legais/Compliance',
            'aprovacoes_necessarias': 'Aprovações Necessárias',
            'campanhas_anteriores_empresa': 'Campanhas Anteriores da Empresa',
            'ticket_medio_atual': 'Ticket Médio Atual (R$)',
            'ticket_medio_desejado': 'Ticket Médio Desejado (R$)',
            'tempo_ciclo_venda': 'Tempo Médio do Ciclo de Venda',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar produtos/serviços baseado no cliente selecionado
        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['produto_servico'].queryset = ProdutoServicoEvento.objects.filter(cliente_id=cliente_id, ativo=True)
            except (ValueError, TypeError):
                self.fields['produto_servico'].queryset = ProdutoServicoEvento.objects.none()
        elif self.instance.pk:
            self.fields['produto_servico'].queryset = self.instance.cliente.produtos_servicos.filter(ativo=True)
        else:
            self.fields['produto_servico'].queryset = ProdutoServicoEvento.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_termino = cleaned_data.get('data_termino')
        
        if data_inicio and data_termino:
            if data_termino <= data_inicio:
                raise forms.ValidationError("A data de término deve ser posterior à data de início.")
        
        return cleaned_data