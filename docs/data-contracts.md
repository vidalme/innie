# Contratos de dados

## Fonte canônica

`metadata.json` aponta para `revisions/NNNNNNNN.json` e contém SHA-256. Recuperar pelo comando state. O snapshot é um objeto com exatamente: schema_version, revision, updated_at, profile, active_cycle, sources, evidence, cycles e changes. Schemas de referência ficam em `schemas`; a validação de runtime combina contratos manuais e checagens semânticas no módulo model.

Schema atual: 1. IDs: até 80 caracteres, letras/números/hífen/underscore, sem separadores de pasta. Datas: AAAA-MM-DD. Campos desconhecidos: null; não usar zero como ausência. Campos específicos podem ser estendidos com metadados descritivos sem mudar os contratos essenciais. Não adicionar novas coleções ao snapshot sem versão/migração.

## Perfil

name, role, seniority, step, area, client, timezone, weekly_capacity_hours, leadership. Pode incluir histórico, objetivos de carreira, promotion_received_on e origem de avaliações. weekly_capacity_hours é disponibilidade de desenvolvimento acordada; não total da jornada. O valor padrão é desconhecido. leadership determina perguntas exclusivas de liderança, não senioridade.

Novos perfis começam com esses campos em null. `leadership: null` significa que ainda falta perguntar; `false` representa uma resposta negativa. DevOps, Operação e America/Fortaleza são sugestões do piloto a confirmar no onboarding. Quando o fuso ainda não foi informado, as visões usam America/Fortaleza provisoriamente e declaram essa suposição; ela não é gravada como resposta no perfil. `status --on DATA` usa a data explícita sem depender de fuso.

## Ciclo

id, label, status, starts_on, ends_on, evidence_cutoff_on, pdi_closes_on, evaluation_on, policy_version, policy_confirmation, milestones e seis coleções: objectives, actions, criterion_assessments, competency_assessments, metrics, events. Milestones contém objetos com `on` e `label`.

Estados: draft, active, archived. Uma pessoa tem no máximo um ciclo ativo. Pode haver vários rascunhos. Arquivado não é editável pelo fluxo comum; adenda separados registram documentos tardios sem alterar o arquivo congelado.

O fechamento do PDI (`pdi_closes_on`) começa desconhecido mesmo quando o corte de evidências está informado. Cada data é preenchida por sua própria informação, via proposta de calendário.

## Fonte

id, kind (personal/institutional/mixed/example), title, original_name, local_path, extracted_path, sha256, imported_at, extraction_status. O import cria estes registros. Um relato ou URL pode ser registrado com ID, kind, title e origem; não presumir arquivo local.

Paths individuais são relativos ao outtie, sem `..` e sem path Windows. Arquivos externos devem ser importados antes de associar local_path. O script de archive recusa path que escape do espaço.

## Evidência

id, title, occurred_on, source_ids, verification e url ou local_path quando houver. Pode incluir contribution, result, audience, duration_hours, inspected_by/at. Situação: claimed, inspected, reviewed, institutionally_confirmed. A última requer confirmation_source. Datas/carga horária sem origem continuam relatadas.

Uma evidência pode estar em vários ciclos, mas sua data real não muda. A validade é interpretada para a data de corte de cada ciclo. Não copiar um critério confirmado do ciclo anterior como atual. Um link inacessível permanece referência informada.

## Objetivo

id, title, description, priority, competency_ids e success_criteria quando apropriado. Horizon pode distinguir ciclo e longo prazo. O produto não força todos os objetivos pessoais a corresponder a critérios de promoção.

## Ação

Obrigatórios: id, title, status. Demais: description, due_on, completed_on, effort_hours, objective_ids, criterion_ids, evidence_ids, source_ids, depends_on, result, pdi_description, external_id, external_registration, carried_from.

Status: proposed, planned, in_progress, done, suspended, cancelled, carried_over. `effort_hours` representa esforço restante estimado; atualizar quando avançar. `done` é realização informada e pode estar sem evidência. Prazo previsto é diferente da execução real. Canceladas/suspensas/transferidas aparecem no painel e não são automaticamente dispensadas de CI-05.

Esforço ausente ou null é desconhecido; zero é uma estimativa explícita de nenhum esforço restante. Para ações planned/in_progress, `status` informa `actions_missing_effort` e a soma conhecida em `known_remaining_effort_hours`. O total `estimated_remaining_effort_hours` fica null enquanto faltar alguma estimativa. `over_capacity` fica null se não for possível concluir; fica true quando a soma conhecida já excede a capacidade calculada, mesmo havendo estimativas pendentes; false exige estimativas completas e capacidade/calendário suficientes para a comparação. A soma continua usando apenas esforço restante, com a margem operacional de 20% já existente.

depends_on referencia IDs do mesmo ciclo; não pode haver dependência circular. objective_ids, source_ids e evidence_ids devem existir. criterion_ids são interpretados conforme a versão institucional selecionada; a relevância é revisada pelo assistente e pelo usuário.

## Avaliação de critério

id, criterion_id, status, evidence_ids, assessed_at/reference_on, reason e confirmation_source quando confirmado. Status: not_applicable, unknown, pending, supported, confirmed, expired. supported significa que o pacote de comprovação parece pertinente, não que a empresa confirmou elegibilidade. confirmed exige origem da confirmação.

## Avaliação técnica

id, skill_id, level, assessment_type (official/self/inferred), assessed_on, assessed_by e source_ids. Comparar nível atual e alvo sem inferir percentual oficial. O cálculo de 70%/100% não foi documentado nos anexos. Inglês tem escala separada.

## Métricas

id, name, value, unit, formula, baseline, period_start/end, source_ids e measurement_type. Antes/depois precisam ter população e janela comparáveis. Relatos diferentes de produtividade ficam separados. Campos quantitativos suportados pela CLI devem ser não negativos; redução é expressa por baseline versus valor atual, não por valor negativo.

## Evento

id, type, description, occurred_on, source_ids, decision e related_action_ids. Fonte original não é apagada após processamento. O import detecta arquivos idênticos; duplicatas semânticas de eventos precisam ser identificadas pelo assistente/usuário.

## Proposta e autorização

Veja [proposals.md](proposals.md). Propostas têm versão esperada e operações, não código executável. `--approve` é confirmação operacional explícita; o CLI não comprova que o modelo realmente pediu autorização. Instruções orientam o assistente a usá-lo corretamente.

## Visões

outputs e exports são derivados. Edição manual detectada impede substituição. `render --preserve-edits` guarda a cópia na inbox e regenera; a interpretação dessa cópia é um fluxo posterior. Não oferece importação semântica automática de qualquer Markdown.

Os novos padrões não reescrevem perfis, estimativas, calendários ou archives existentes. Valores antigos que tenham sido presumidos precisam de revisão por proposta; não há como distinguir automaticamente um zero informado de um zero colocado anteriormente como padrão. A leitura atual continua aceitando estados anteriores do schema 1.

## Orientação de início e retomada

`onboarding` deriva a etapa de atendimento do snapshot, das propostas sem recibo de aplicação e da existência de `inbox/onboarding.md`. Não adiciona coleções ao schema nem grava respostas automaticamente. `career_goal` é uma extensão descritiva opcional do perfil; objetivos existentes no ciclo também suprem essa pergunta.

Respostas candidatas ficam nas notas/propostas, com origem e situação. Somente `apply` após autorização as incorpora ao estado canônico. Propostas de revisão anterior são exibidas como `stale`; o assistente confere decisões de recusa/substituição nas notas antes de reapresentá-las. O comando não interpreta o conteúdo das notas nem elimina propostas antigas. Campos faltantes são orientação, não um bloqueio a rascunhos provisórios.

`status` preserva os indicadores de ciclo e acrescenta `onboarding`. Sem ativo ou seleção explícita, retorna `status: no_active_cycle`, `cycle_id: null` e orientação com rascunhos disponíveis. Sem metadata, retorna `setup_required`. Nenhuma dessas consultas cria ou ativa um ciclo; `--cycle ID` permite consultar um rascunho sem ativá-lo.
