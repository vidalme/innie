"""Orientação de início/retomada derivada do estado e de propostas persistidas."""
from __future__ import annotations

from pathlib import Path

from .model import PDIError, cycle
from .operations import policy_alignment
from .storage import inside, read_json
from .views import overview

PROFILE_QUESTIONS = {
    'role': 'Qual é sua função atual?',
    'seniority': 'Qual é sua senioridade atual?',
    'area': 'Em qual área você atua?',
    'career_goal': 'O que você quer desenvolver ou alcançar neste ciclo?',
    'weekly_capacity_hours': 'Quantas horas por semana você tem disponíveis para esse desenvolvimento?',
    'timezone': 'Qual é seu fuso horário?',
    'leadership': 'Você atua formalmente em liderança?',
}
CALENDAR_FIELDS = ('starts_on', 'ends_on', 'evidence_cutoff_on', 'pdi_closes_on', 'evaluation_on')
FIELD_LABELS = {'role': 'função', 'seniority': 'senioridade', 'area': 'área',
                'career_goal': 'objetivo', 'weekly_capacity_hours': 'disponibilidade semanal',
                'timezone': 'fuso horário', 'leadership': 'atuação em liderança',
                'starts_on': 'início', 'ends_on': 'fim', 'evidence_cutoff_on': 'corte de evidências',
                'pdi_closes_on': 'fechamento do PDI', 'evaluation_on': 'avaliação'}
STAGE_LABELS = {'setup_required': 'preparar o espaço', 'archived': 'ciclo arquivado',
                'proposal_check_required': 'conferir propostas', 'proposal_review': 'revisar propostas',
                'cycle_selection': 'escolher ciclo', 'tracking': 'acompanhamento',
                'profile_incomplete': 'completar contexto', 'calendar_incomplete': 'confirmar calendário',
                'plan_building': 'preparar plano', 'activation_review': 'revisar ativação'}

def pending_proposals(store, revision):
    pending, issues = [], []
    folder = inside(store.root, store.root / 'proposals')
    for path in sorted(folder.glob('*.json')):
        try:
            path = inside(folder, path)
            proposal = read_json(path)
            if not isinstance(proposal, dict) or proposal.get('schema_version') != 1 or proposal.get('id') != path.stem:
                raise PDIError('ID da proposta difere do nome do arquivo.')
            expected = proposal.get('expected_revision')
            if type(expected) is not int or expected < 0 or not isinstance(proposal.get('operations'), list):
                raise PDIError('Proposta sem revisão/operações válidas.')
            receipt = inside(store.root, store.root / 'operations' / path.name)
            if receipt.exists():
                continue
            pending.append({'id': proposal['id'], 'path': str(path), 'reason': proposal.get('reason'),
                            'expected_revision': expected,
                            'status': 'awaiting_review' if expected == revision else 'stale'})
        except (PDIError, OSError) as exc:
            issues.append({'path': str(path), 'error': str(exc)})
    return pending, issues

def guidance(store, cycle_id=None, state=None, innie=None):
    """Somente leitura: respostas candidatas nunca viram fatos por esta consulta."""
    if state is None:
        if not (store.root / 'metadata.json').exists():
            return {'revision': None, 'active_cycle': None, 'selected_cycle': None, 'cycles': [],
                    'stage': 'setup_required', 'next_steps': ['Execute bash scripts/bootstrap.sh e confira o assistente no editor.'],
                    'questions': [], 'pending_proposals': [], 'proposal_issues': [], 'resume_notes': []}
        state = store.load()
    selected = cycle(state, cycle_id) if cycle_id else (cycle(state) if state['active_cycle'] else None)
    profile = state['profile']
    missing_profile = [key for key in PROFILE_QUESTIONS if profile.get(key) in (None, '')
                       and not (key == 'career_goal' and selected and selected['objectives'])]
    missing_calendar = [key for key in CALENDAR_FIELDS if selected and not selected.get(key)]
    proposals, issues = pending_proposals(store, state['revision'])
    note = inside(store.root, store.root / 'inbox/onboarding.md')
    result = {'revision': state['revision'], 'active_cycle': state['active_cycle'],
              'selected_cycle': selected['id'] if selected else None,
              'cycles': [{'id': c['id'], 'label': c['label'], 'status': c['status']} for c in state['cycles']],
              'profile': profile, 'missing_profile': missing_profile, 'missing_calendar': missing_calendar,
              'source_count': len(state['sources']), 'pending_proposals': proposals, 'proposal_issues': issues,
              'resume_notes': [str(note)] if note.is_file() else [], 'questions': []}
    if innie is not None:
        result['policy_alignment'] = policy_alignment(innie, selected)
    if selected and selected['status'] == 'archived':
        stage, step = 'archived', 'Consulte o archive deste ciclo; para continuar, escolha um ciclo aberto.'
    elif issues:
        stage, step = 'proposal_check_required', 'Confira os arquivos de proposta indicados antes de retomar alterações.'
    elif proposals:
        stage, step = 'proposal_review', 'Leia as propostas pendentes e as respostas já registradas antes de perguntar novamente. Propostas stale precisam ser refeitas contra a revisão atual.'
    elif not selected:
        drafts = [c for c in state['cycles'] if c['status'] == 'draft']
        stage, step = 'cycle_selection', 'Escolha o ciclo a retomar; consulte um rascunho com --cycle ID.' if drafts else 'Confirme se já existe PDI ou rascunho antes de criar um ciclo.'
        result['questions'] = ['Qual rascunho deseja retomar?'] if drafts else ['Você já tem um PDI ou rascunho para este período?']
    elif selected['status'] == 'active' and selected['actions']:
        stage, step = 'tracking', 'Revise os próximos passos, atrasos e evidências; use /pdi-atualizar para registrar uma novidade.'
    elif missing_profile:
        stage, step = 'profile_incomplete', 'Complete apenas as informações necessárias ao próximo resultado; desconhecidos podem permanecer pendentes.'
        result['questions'] = [PROFILE_QUESTIONS[key] for key in missing_profile[:2]]
    elif any(key in missing_calendar for key in CALENDAR_FIELDS[:3]):
        stage, step = 'calendar_incomplete', 'Mantenha o ciclo como rascunho enquanto início, fim ou corte estiverem desconhecidos; o plano provisório pode avançar.'
        result['questions'] = ['Quais datas de início, fim e corte de evidências você já conhece?']
    elif not selected['actions']:
        stage, step = 'plan_building', ('Revise as fontes importadas e prepare a proposta de plano.' if state['sources'] else
                                      'Comece com um relato de objetivo e compromissos ou importe um PDI; documentos são opcionais para o rascunho.')
    else:
        stage, step = 'activation_review', 'Revise calendário, plano e regras antes de ativar o rascunho.'
    result.update(stage=stage, next_steps=[step])
    if result['resume_notes']:
        result['next_steps'].insert(0, 'Leia inbox/onboarding.md; suas respostas são candidatas até serem incorporadas por proposta aprovada.')
    return result

def status_report(store, cycle_id=None, on=None):
    if not (store.root / 'metadata.json').exists():
        return {'revision': None, 'cycle_id': None, 'status': 'setup_required',
                'onboarding': guidance(store, cycle_id)}
    state = store.load()
    onboarding = guidance(store, cycle_id, state, Path(__file__).resolve().parents[2])
    selected = onboarding['selected_cycle']
    result = overview(state, selected, on) if selected else {'revision': state['revision'], 'cycle_id': None, 'status': 'no_active_cycle'}
    result['onboarding'] = onboarding
    return result

def guidance_text(result):
    context = result.get('onboarding', result)
    lines = [f"Etapa: {STAGE_LABELS[context['stage']]}", f"Revisão: {context['revision'] if context['revision'] is not None else 'espaço não preparado'}",
             f"Ciclo ativo: {context['active_cycle'] or 'nenhum'}",
             f"Ciclo consultado: {context['selected_cycle'] or 'nenhum'}"]
    lines.extend(f"- {c['id']}: {c['label']} ({c['status']})" for c in context['cycles'])
    lines.extend(f"- Proposta {p['id']}: {p['status']} — {p['path']}" for p in context['pending_proposals'])
    lines.extend(f"- Conferir proposta: {p['path']} — {p['error']}" for p in context['proposal_issues'])
    lines.extend(f"- Respostas em rascunho: {p}" for p in context['resume_notes'])
    if context.get('missing_profile'):
        lines.append('Perfil a completar: ' + ', '.join(FIELD_LABELS[key] for key in context['missing_profile']))
    if context.get('missing_calendar'):
        lines.append('Datas a confirmar: ' + ', '.join(FIELD_LABELS[key] for key in context['missing_calendar']))
    alignment = context.get('policy_alignment')
    if alignment and not alignment['aligned']:
        lines.append('Política divergente: confira a versão do ciclo e os artefatos institucionais antes de usar critérios ou fechar.')
    if 'late_actions' in result:
        lines.extend([f"Ações em atraso: {', '.join(result['late_actions']) or 'nenhuma identificada'}",
                      f"Realizadas sem evidência: {', '.join(result['done_without_evidence']) or 'nenhuma identificada'}",
                      f"Esforço conhecido: {result['known_remaining_effort_hours']} h; estimativas pendentes: {', '.join(result['actions_missing_effort']) or 'nenhuma'}"])
    lines.extend(['', 'Próximos passos:', *context['next_steps']])
    if context['questions']:
        lines.extend(['Perguntas sugeridas (confira respostas já registradas):', *context['questions']])
    return '\n'.join(lines)
