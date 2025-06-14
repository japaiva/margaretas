# core/forms/cliente.py - VERSÃO SIMPLIFICADA

from django import forms
from core.models import Cliente, ProdutoServicoEvento, Campanha
from core.utils.view_utils import DateAwareModelForm
from decimal import Decimal, InvalidOperation
import re


class ClienteForm(DateAwareModelForm):
    """Formulário para cadastro de clientes - APENAS NOME DA EMPRESA OBRIGATÓRIO"""
    
    # SOBRESCREVER os campos monetários para usar CharField com validação customizada
    faturamento_anual = forms.CharField(
        label='Faturamento Anual Estimado (R$)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1.000.000,00 ou 1000000'
        }),
        help_text='Digite o valor em qualquer formato (ex: 1.000.000,50 ou 1000000.50)'
    )
    
    orcamento_marketing = forms.CharField(
        label='Orçamento de Marketing (R$)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50.000,00 ou 50000'
        }),
        help_text='Digite o valor em qualquer formato (ex: 50.000,00 ou 50000.00)'
    )
    
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
            # === CAMPO OBRIGATÓRIO ===
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome da empresa ou marca',
                'required': True  # Enfatizar que é obrigatório
            }),
            
            # === CAMPOS OPCIONAIS ===
            'cnpj_cpf': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '00.000.000/0000-00 ou 000.000.000-00'
            }),
            'endereco_completo': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Endereço completo da empresa'
            }),
            
            # === RESPONSÁVEIS (TODOS OPCIONAIS) ===
            'responsavel_contrato': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome completo (opcional)'
            }),
            'cargo_responsavel': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cargo na empresa (opcional)'
            }),
            'contato_responsavel': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email ou telefone (opcional)'
            }),
            'pessoa_contato_tecnico': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome completo (opcional)'
            }),
            'contato_tecnico': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email ou telefone (opcional)'
            }),
            
            # === TEXTO LONGO (TODOS OPCIONAIS) ===
            'historia_empresa': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Conte a história da empresa, marcos importantes, evolução... (opcional)'}),
            'missao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual é a missão da empresa? (opcional)'}),
            'visao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual é a visão da empresa? (opcional)'}),
            'valores': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais são os valores da empresa? (opcional)'}),
            'lista_produtos_servicos': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva os produtos ou serviços oferecidos (opcional)'}),
            
            # === PÚBLICO-ALVO (TODOS OPCIONAIS) ===
            'descricao_publico': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Idade, gênero, interesses, comportamentos... (opcional)'}),
            'necessidades_desejos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que o público busca? Quais são suas dores? (opcional)'}),
            'comportamento_compra': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como o público costuma comprar? (opcional)'}),
            'consideracoes_demograficas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Onde está localizado? Onde quer atingir? (opcional)'}),
            'niveis_consciencia': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Nível de conhecimento sobre o produto/serviço (opcional)'}),
            'objecoes_comuns': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Preço, tempo, confiança, etc. (opcional)'}),
            'tentativas_passadas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que já tentaram e não funcionou? (opcional)'}),
            
            # === POSICIONAMENTO (TODOS OPCIONAIS) ===
            'posicionamento_atual': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como a marca está posicionada hoje? (opcional)'}),
            'objetivos_posicionamento': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como querem ser percebidos? (opcional)'}),
            'diferenciacao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que os diferencia da concorrência? (opcional)'}),
            
            # === COMUNICAÇÃO (TODOS OPCIONAIS) ===
            'tom_voz': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Formal, descontraído, técnico, amigável... (opcional)'}),
            'mensagem_principal': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Qual mensagem principal querem transmitir? (opcional)'}),
            'manifesto_marca': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Manifesto ou propósito da marca (opcional)'}),
            'canais_comunicacao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Redes sociais, site, email... (inclua links/perfis) (opcional)'}),
            
            # === OBJETIVOS (TODOS OPCIONAIS) ===
            'objetivos_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais são os objetivos de marketing? (opcional)'}),
            'metas_especificas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Metas mensuráveis e específicas (opcional)'}),
            'kpis_empresa': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Como medem o sucesso? (opcional)'}),
            
            # === CONCORRÊNCIA (TODOS OPCIONAIS) ===
            'analise_concorrencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Principais concorrentes (incluir sites/perfis) (opcional)'}),
            'pontos_fortes_fracos_concorrencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que fazem bem e onde falham? (opcional)'}),
            
            # === RECURSOS (TODOS OPCIONAIS) ===
            'equipe_marketing': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quem é a equipe responsável? (opcional)'}),
            'recursos_tecnologicos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ferramentas e tecnologias disponíveis (opcional)'}),
            
            # === EXPECTATIVAS (TODOS OPCIONAIS) ===
            'expectativas_agencia': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que esperam da parceria? (opcional)'}),
            'resultados_esperados': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Que resultados esperam? (opcional)'}),
            
            # === CAMPOS OPCIONAIS ===
            'experiencia_agencias': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Já trabalharam com outras agências? Como foi? (opcional)'}),
            'criativos_performaram': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quais materiais funcionaram bem? (opcional)'}),
            'analise_campanhas_anteriores': forms.Textarea(attrs={'rows': 4, 'placeholder': 'O que funcionou ou não funcionou? (opcional)'}),
            
            # === DIGITAL (TODOS OPCIONAIS) ===
            'website_principal': forms.URLInput(attrs={'placeholder': 'https://exemplo.com.br (opcional)'}),
            'outros_dominios': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Outros sites ou domínios da empresa (opcional)'}),
            'crm_utilizado': forms.TextInput(attrs={'placeholder': 'Ex: Pipedrive, Salesforce, RD Station (opcional)'}),
            
            # === CONTEXTO ADICIONAL (TODOS OPCIONAIS) ===
            'principais_desafios': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Principais desafios do mercado atual (opcional)'}),
            'sazonalidades': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Períodos de alta/baixa, datas importantes (opcional)'}),
            'certificacoes_diferenciais': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Certificações, prêmios, diferenciais técnicos (opcional)'}),
            
            # === CHECKBOXES ===
            'manual_marca': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'google_analytics': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tag_manager': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pixel_facebook': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            # ÚNICO CAMPO OBRIGATÓRIO
            'nome_empresa': 'Nome da Empresa/Marca *',
            
            # TODOS OS OUTROS SÃO OPCIONAIS (remover asteriscos)
            'cnpj_cpf': 'CNPJ/CPF',
            'endereco_completo': 'Endereço Completo',
            'historia_empresa': 'História da Empresa',
            'missao': 'Missão da Empresa',
            'visao': 'Visão da Empresa',
            'valores': 'Valores da Empresa',
            'lista_produtos_servicos': 'Produtos ou Serviços',
            'responsavel_contrato': 'Responsável pelo Contrato',
            'cargo_responsavel': 'Cargo do Responsável',
            'contato_responsavel': 'Contato do Responsável',
            'pessoa_contato_tecnico': 'Pessoa de Contato Técnico',
            'contato_tecnico': 'Contato da Pessoa Técnica',
            'descricao_publico': 'Descrição do Público-Alvo',
            'necessidades_desejos': 'Necessidades e Desejos do Público',
            'comportamento_compra': 'Comportamento de Compra',
            'consideracoes_demograficas': 'Considerações Demográficas',
            'niveis_consciencia': 'Níveis de Consciência sobre o Serviço',
            'objecoes_comuns': 'Objeções ou Resistências Comuns',
            'tentativas_passadas': 'O que Já Tentaram e Não Funcionou',
            'posicionamento_atual': 'Posicionamento Atual',
            'objetivos_posicionamento': 'Objetivos de Posicionamento',
            'diferenciacao': 'Diferenciação vs Concorrência',
            'tom_voz': 'Tom e Voz da Marca',
            'mensagem_principal': 'Mensagem Principal',
            'manual_marca': 'Possui Manual de Marca?',
            'manifesto_marca': 'Manifesto da Marca',
            'canais_comunicacao': 'Canais de Comunicação e Perfis',
            'objetivos_marketing': 'Objetivos de Marketing',
            'metas_especificas': 'Metas Específicas',
            'kpis_empresa': 'KPIs da Empresa',
            'analise_concorrencia': 'Análise da Concorrência',
            'pontos_fortes_fracos_concorrencia': 'Pontos Fortes e Fracos da Concorrência',
            'equipe_marketing': 'Equipe de Marketing',
            'recursos_tecnologicos': 'Recursos Tecnológicos',
            'expectativas_agencia': 'Expectativas da Agência',
            'resultados_esperados': 'Resultados Esperados',
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
        # Adicionar classe form-control para todos os campos que não têm
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.TextInput, forms.Textarea, forms.URLInput]:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'

    def _convert_money_value(self, value):
        """Função auxiliar para converter valores monetários"""
        if not value:
            return None
            
        # Converter para string e limpar
        value = str(value).strip()
        if value == '':
            return None
            
        # Remover símbolos monetários e espaços (incluindo &nbsp;)
        value = re.sub(r'[R$\s\xa0]', '', value)
        
        # Tratar formato brasileiro vs americano
        if ',' in value and '.' in value:
            # Se vírgula vem depois do último ponto = formato brasileiro (1.234.567,89)
            if value.rindex(',') > value.rindex('.'):
                value = value.replace('.', '').replace(',', '.')
            else:
                # Formato americano (1,234,567.89)
                value = value.replace(',', '')
        elif ',' in value:
            # Só vírgula - verificar se é decimal ou separador
            parts = value.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Decimal brasileiro: 1234,50
                value = value.replace(',', '.')
            else:
                # Separador: 1,234,567
                value = value.replace(',', '')
        
        # Limpar caracteres inválidos (manter apenas números e ponto)
        value = re.sub(r'[^0-9.]', '', value)
        
        # Garantir que só tenha um ponto decimal
        if value.count('.') > 1:
            parts = value.split('.')
            value = ''.join(parts[:-1]) + '.' + parts[-1]
        
        try:
            return Decimal(value) if value else None
        except (InvalidOperation, ValueError):
            return None

    def clean_faturamento_anual(self):
        """Limpa e converte o campo de faturamento anual"""
        value = self.cleaned_data.get('faturamento_anual')
        converted = self._convert_money_value(value)
        
        if converted is None and value and value.strip():
            # Se tinha valor mas não conseguiu converter
            raise forms.ValidationError(
                'Por favor, insira um valor numérico válido para o faturamento anual. '
                'Exemplos: 1000000, 1000000.50, 1.000.000,50'
            )
        
        return converted

    def clean_orcamento_marketing(self):
        """Limpa e converte o campo de orçamento de marketing"""
        value = self.cleaned_data.get('orcamento_marketing')
        converted = self._convert_money_value(value)
        
        if converted is None and value and value.strip():
            # Se tinha valor mas não conseguiu converter
            raise forms.ValidationError(
                'Por favor, insira um valor numérico válido para o orçamento de marketing. '
                'Exemplos: 50000, 50000.00, 50.000,00'
            )
        
        return converted
    
    def clean_arquetipos(self):
        """Valida seleção de arquétipos"""
        arquetipos = self.cleaned_data.get('arquetipos', [])
        if len(arquetipos) > 3:
            raise forms.ValidationError("Selecione no máximo 3 arquétipos.")
        return arquetipos

    def clean_nome_empresa(self):
        """Validação específica para o único campo obrigatório"""
        nome = self.cleaned_data.get('nome_empresa')
        if not nome or not nome.strip():
            raise forms.ValidationError('O nome da empresa é obrigatório.')
        return nome.strip()


# Manter as outras classes inalteradas
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
        ('Google Search', 'Google Ads - Search'),
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
            
            # Orçamento e cronograma
            'orcamento_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ex: 10000.00'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            # Monitoramento
            'frequencia_monitoramento': forms.Select(attrs={'class': 'form-select'}),
            'estrategias_otimizacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ajustes de lances, anúncios, audiences'}),
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
            self.fields['produto_servico'].queryset = self.instance.cliente.produtos_servicos_relacionados.filter(ativo=True)
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