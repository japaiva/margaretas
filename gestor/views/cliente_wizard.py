# gestor/views/cliente.py - SUBSTITUIR A CLASSE ClienteWizardView EXISTENTE

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import JsonResponse
from formtools.wizard.views import SessionWizardView

from core.models import Cliente
from core.forms.wizard_forms import (
    ClienteWizardStep1Form, 
    ClienteWizardStep2Form, 
    ClienteWizardStep3Form,
    ClienteWizardStep4Form, 
    ClienteWizardStep5Form, 
    ClienteWizardStep6Form
)

import logging
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class ClienteWizardView(SessionWizardView):
    """Wizard completo para cadastro detalhado de cliente em 6 steps"""
    
    form_list = [
        ('step1', ClienteWizardStep1Form),
        ('step2', ClienteWizardStep2Form), 
        ('step3', ClienteWizardStep3Form),
        ('step4', ClienteWizardStep4Form),
        ('step5', ClienteWizardStep5Form),
        ('step6', ClienteWizardStep6Form),
    ]
    
    def dispatch(self, request, *args, **kwargs):
        # Verificar se cliente existe para edição
        self.cliente_id = kwargs.get('pk')
        if self.cliente_id:
            self.cliente = get_object_or_404(Cliente, pk=self.cliente_id)
        else:
            self.cliente = None
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_template_names(self):
        """Retorna template específico para cada step"""
        current_step = self.steps.current
        
        template_mapping = {
            'step1': 'gestor/cliente/wizard/step1.html',
            'step2': 'gestor/cliente/wizard/step2.html',
            'step3': 'gestor/cliente/wizard/step3.html',
            'step4': 'gestor/cliente/wizard/step4.html',
            'step5': 'gestor/cliente/wizard/step5.html',
            'step6': 'gestor/cliente/wizard/step6.html',
        }
        
        return [template_mapping.get(current_step, 'gestor/cliente/wizard/step1.html')]
    
    def get_form_initial(self, step):
        """Preencher form com dados existentes do cliente"""
        initial = super().get_form_initial(step)
        
        if self.cliente:
            # Mapear campos para cada step
            field_mapping = {
                'step1': [
                    'nome_empresa', 'ativo', 'cnpj_cpf', 'endereco_completo',
                    'responsavel_contrato', 'cargo_responsavel', 'contato_responsavel',
                    'pessoa_contato_tecnico', 'contato_tecnico', 'faturamento_anual',
                    'lista_produtos_servicos', 'website_principal', 'outros_dominios'
                ],
                'step2': [
                    'descricao_publico', 'consideracoes_demograficas', 'niveis_consciencia',
                    'necessidades_desejos', 'comportamento_compra', 'objecoes_comuns',
                    'tentativas_passadas'
                ],
                'step3': [
                    'posicionamento_atual', 'objetivos_posicionamento', 'diferenciacao',
                    'tom_voz', 'mensagem_principal', 'manifesto_marca', 
                    'canais_comunicacao', 'manual_marca', 'arquetipos'
                ],
                'step4': [
                    'objetivos_marketing', 'metas_especificas', 'kpis_empresa',
                    'analise_concorrencia', 'pontos_fortes_fracos_concorrencia'
                ],
                'step5': [
                    'orcamento_marketing', 'crm_utilizado', 'equipe_marketing', 
                    'recursos_tecnologicos', 'google_analytics', 'tag_manager', 
                    'pixel_facebook', 'expectativas_agencia', 'resultados_esperados',
                    'experiencia_agencias', 'criativos_performaram', 'analise_campanhas_anteriores',
                    'principais_desafios', 'sazonalidades', 'certificacoes_diferenciais'
                ]
                # step6 não precisa de initial pois é só confirmação
            }
            
            # Preencher campos do step atual
            if step in field_mapping:
                for field in field_mapping[step]:
                    if hasattr(self.cliente, field):
                        value = getattr(self.cliente, field)
                        if value is not None:
                            # Converter valores monetários para string para exibição
                            if field in ['faturamento_anual', 'orcamento_marketing'] and value:
                                initial[field] = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                            else:
                                initial[field] = value
        
        return initial
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        
        # Adicionar informações do cliente
        context['cliente'] = self.cliente
        context['title'] = f'Wizard: {self.cliente.nome_empresa}' if self.cliente else 'Novo Cliente'
        
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
                'step1': 'Informações Básicas',
                'step2': 'Público-Alvo', 
                'step3': 'Posicionamento',
                'step4': 'Objetivos',
                'step5': 'Recursos',
                'step6': 'Confirmação'
            }
        })
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Override para tratar actions especiais"""
        
        # Verificar se é uma ação especial (save_draft, finish)
        action = request.POST.get('action')
        
        if action in ['save_draft', 'finish']:
            return self.handle_special_action(request, action)
        
        # Continuar com o processamento normal do wizard
        return super().post(request, *args, **kwargs)
    
    def handle_special_action(self, request, action):
        """Tratar ações especiais como save_draft e finish"""
        
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
            
            # Se não tem cliente, criar um novo
            if not self.cliente:
                self.cliente = Cliente()
                self.cliente.created_by = request.user
            
            # Aplicar dados coletados
            for field, value in all_data.items():
                if hasattr(self.cliente, field) and field != 'confirmar_dados':
                    setattr(self.cliente, field, value)
            
            # Salvar cliente
            self.cliente.save()
            
            if action == 'save_draft':
                return JsonResponse({
                    'success': True,
                    'message': 'Rascunho salvo com sucesso!',
                    'cliente_id': str(self.cliente.pk)
                })
            
            elif action == 'finish':
                # Limpar dados do wizard da sessão
                self.storage.reset()
                
                messages.success(
                    request, 
                    f'Cliente "{self.cliente.nome_empresa}" salvo com sucesso! '
                    f'Briefing completo finalizado.'
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Cliente cadastrado com sucesso!',
                    'redirect_url': f'/gestor/clientes/{self.cliente.pk}/'
                })
        
        except Exception as e:
            logger.error(f"Erro ao salvar cliente: {e}")
            return JsonResponse({
                'success': False,
                'message': f'Erro ao salvar: {str(e)}'
            })
    
    def done(self, form_list, **kwargs):
        """Processar dados finais do wizard - método obrigatório"""
        
        # Se não tem cliente, criar um novo
        if not self.cliente:
            self.cliente = Cliente()
            self.cliente.created_by = self.request.user
        
        # Aplicar dados de todos os forms (exceto step6 que é só confirmação)
        for step, form in zip(self.form_list.keys(), form_list):
            if step != 'step6':  # Pular step6 pois é só confirmação
                for field, value in form.cleaned_data.items():
                    if hasattr(self.cliente, field):
                        setattr(self.cliente, field, value)
        
        # Salvar cliente
        self.cliente.save()
        
        messages.success(
            self.request, 
            f'Cliente "{self.cliente.nome_empresa}" salvo com sucesso! '
            f'Briefing completo finalizado em 6 etapas.'
        )
        
        return redirect('gestor:cliente_detail', pk=self.cliente.pk)