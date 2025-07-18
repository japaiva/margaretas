# gestor/views/cliente_wizard.py - VERSÃO REFATORADA (5 STEPS)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from formtools.wizard.views import SessionWizardView

from core.models import Cliente
from core.forms.wizard_forms import (
    ClienteWizardStep1Form,  # História
    ClienteWizardStep2Form,  # Posicionamento e Comunicação
    ClienteWizardStep3Form,  # Objetivos e Estratégia
    ClienteWizardStep4Form,  # Público-Alvo
    ClienteWizardStep5Form,  # Recursos e Expectativas
    ClienteWizardConfirmForm  # Confirmação final
)

import logging
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class ClienteWizardView(SessionWizardView):
    """Wizard para briefing estratégico de cliente em 5 steps focados"""
    
    form_list = [
        ('historia', ClienteWizardStep1Form),        # 1. História da Empresa
        ('posicionamento', ClienteWizardStep2Form),  # 2. Posicionamento e Comunicação
        ('objetivos', ClienteWizardStep3Form),       # 3. Objetivos e Estratégia
        ('publico_alvo', ClienteWizardStep4Form),    # 4. Público-Alvo
        ('recursos', ClienteWizardStep5Form),        # 5. Recursos e Expectativas
    ]
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar se cliente existe para edição
        self.cliente_id = kwargs.get('pk')
        if self.cliente_id:
            self.cliente = get_object_or_404(Cliente, pk=self.cliente_id)
        else:
            # Para wizard de briefing, cliente deve existir (foi criado no form simples)
            messages.error(request, 'Cliente deve ser criado primeiro usando o cadastro rápido.')
            return redirect('gestor:cliente_list')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_template_names(self):
        """Retorna template específico para cada step"""
        current_step = self.steps.current
        
        template_mapping = {
            'historia': 'gestor/cliente/wizard/historia.html',
            'posicionamento': 'gestor/cliente/wizard/posicionamento.html',
            'objetivos': 'gestor/cliente/wizard/objetivos.html',
            'publico_alvo': 'gestor/cliente/wizard/publico_alvo.html',
            'recursos': 'gestor/cliente/wizard/recursos.html',
        }
        
        return [template_mapping.get(current_step, 'gestor/cliente/wizard/historia.html')]
    
    def get_form_initial(self, step):
        """Preencher form com dados existentes do cliente"""
        initial = super().get_form_initial(step)
        
        if self.cliente:
            # Mapear campos para cada step
            field_mapping = {
                'historia': [
                    'historia_empresa', 'missao', 'visao', 'valores'
                ],
                'posicionamento': [
                    'posicionamento_atual', 'objetivos_posicionamento', 'diferenciacao',
                    'tom_voz', 'mensagem_principal', 'manifesto_marca', 
                    'canais_comunicacao', 'manual_marca', 'arquetipos'
                ],
                'objetivos': [
                    'objetivos_marketing', 'metas_especificas', 'kpis_empresa',
                    'analise_concorrencia', 'pontos_fortes_fracos_concorrencia'
                ],
                'publico_alvo': [
                    'descricao_publico', 'necessidades_desejos', 'comportamento_compra',
                    'consideracoes_demograficas', 'niveis_consciencia', 
                    'objecoes_comuns', 'tentativas_passadas'
                ],
                'recursos': [
                    'orcamento_marketing', 'equipe_marketing', 'recursos_tecnologicos',
                    'expectativas_agencia', 'resultados_esperados',
                    'experiencia_agencias', 'criativos_performaram', 
                    'analise_campanhas_anteriores', 'google_analytics', 
                    'tag_manager', 'pixel_facebook', 'crm_utilizado',
                    'principais_desafios', 'sazonalidades', 'certificacoes_diferenciais'
                ]
            }
            
            # Preencher campos do step atual
            if step in field_mapping:
                for field in field_mapping[step]:
                    if hasattr(self.cliente, field):
                        value = getattr(self.cliente, field)
                        if value is not None:
                            # Converter valores monetários para string para exibição
                            if field == 'orcamento_marketing' and value:
                                initial[field] = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                            else:
                                initial[field] = value
        
        return initial
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        
        # Adicionar informações do cliente
        context['cliente'] = self.cliente
        context['title'] = f'Briefing Estratégico: {self.cliente.nome_empresa}'
        
        # Progress e step info
        current_step = self.steps.current
        total_steps = self.steps.count
        step_index = self.steps.index
        
        context.update({
            'current_step': current_step,
            'total_steps': total_steps,
            'step_index': step_index,
            'progress_percent': ((step_index + 1) / total_steps) * 100,
            'step_names': {
                'historia': 'História',
                'posicionamento': 'Posicionamento', 
                'objetivos': 'Objetivos',
                'publico_alvo': 'Público-Alvo',
                'recursos': 'Recursos'
            }
        })
        
        # Progresso do briefing
        context['briefing_progress'] = self.cliente.briefing_progress
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Override para tratar actions especiais"""
        
        # Verificar se é uma ação especial (save_draft, finish)
        action = request.POST.get('action')
        
        logger.info(f"Wizard POST - Action: {action}")  # Debug log
        
        if action in ['save_draft', 'finish']:
            logger.info(f"Processando ação especial: {action}")  # Debug log
            return self.handle_special_action(request, action)
        
        # Continuar com o processamento normal do wizard
        logger.info("Processamento normal do wizard")  # Debug log
        return super().post(request, *args, **kwargs)
    
    def handle_special_action(self, request, action):
        """Tratar ações especiais como save_draft e finish"""
        
        logger.info(f"handle_special_action chamado - Action: {action}")  # Debug log
        
        try:
            # Obter dados de todos os steps salvos até agora
            all_data = {}
            
            # Coletar dados de todos os steps válidos
            for step_name in self.get_form_list():
                step_data = self.storage.get_step_data(step_name)
                if step_data:
                    # Validar o form para garantir que os dados estão corretos
                    form_class = self.form_list[step_name]
                    form = form_class(step_data, prefix=self.get_form_prefix(step_name, form_class))
                    
                    if form.is_valid():
                        all_data.update(form.cleaned_data)
                        logger.debug(f"Dados válidos para step {step_name}")
                    else:
                        logger.warning(f"Dados inválidos para step {step_name}: {form.errors}")
            
            logger.info(f"Total de campos coletados: {len(all_data)}")
            
            # Aplicar dados coletados ao cliente existente
            for field, value in all_data.items():
                if hasattr(self.cliente, field):
                    setattr(self.cliente, field, value)
                else:
                    logger.warning(f"Campo {field} não existe no modelo Cliente")
            
            # Se está finalizando, marcar briefing como completo
            if action == 'finish':
                self.cliente.briefing_completo = True
                self.cliente.data_briefing = timezone.now()
                logger.info("Briefing marcado como completo")
            
            # Salvar cliente
            self.cliente.save()
            logger.info(f"Cliente {self.cliente.nome_empresa} salvo com sucesso")
            
            if action == 'save_draft':
                return JsonResponse({
                    'success': True,
                    'message': 'Rascunho do briefing salvo com sucesso!',
                    'cliente_id': str(self.cliente.pk),
                    'progress': self.cliente.briefing_progress
                })
            
            elif action == 'finish':
                # Limpar dados do wizard da sessão
                self.storage.reset()
                
                messages.success(
                    request, 
                    f'Briefing estratégico de "{self.cliente.nome_empresa}" finalizado com sucesso! '
                    f'Agora você pode criar campanhas de marketing.'
                )
                
                # SEMPRE fazer redirect direto para submissão normal do form
                return redirect('gestor:cliente_detail', pk=self.cliente.pk)
        
        except Exception as e:
            logger.error(f"Erro ao salvar briefing do cliente: {e}", exc_info=True)
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar briefing: {str(e)}'
            })
    
    def done(self, form_list, **kwargs):
        """Processar dados finais do wizard - método obrigatório"""
        
        # Aplicar dados de todos os forms
        for step, form in zip(self.form_list.keys(), form_list):
            for field, value in form.cleaned_data.items():
                if hasattr(self.cliente, field):
                    setattr(self.cliente, field, value)
        
        # Marcar briefing como completo
        self.cliente.briefing_completo = True
        self.cliente.data_briefing = timezone.now()
        
        # Salvar cliente
        self.cliente.save()
        
        messages.success(
            self.request, 
            f'Briefing estratégico de "{self.cliente.nome_empresa}" finalizado com sucesso! '
            f'Todas as informações foram salvas e agora você pode criar campanhas de marketing.'
        )
        
        return redirect('gestor:cliente_detail', pk=self.cliente.pk)