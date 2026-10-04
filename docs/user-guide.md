# Guia do colaborador

## Primeiro uso ou retomada

Selecionar copiloto-desenvolvimento e conversar normalmente. Não precisa memorizar comandos ou escolher especialistas. Explicar objetivo, cargo/nível e período. Se já houver plano, dizer “Já tenho PDI; quero planejar o restante do ciclo”. O assistente deve recuperar o estado e pedir só o que falta.

Em um perfil novo, cargo, área, atuação em liderança e fuso horário começam pendentes. DevOps, Operação e America/Fortaleza podem ser sugeridos para este piloto; confirme o que se aplica a você. Informe o fechamento do PDI separadamente do corte de evidências. Se já houver valores registrados de uma versão anterior, revise-os com o assistente antes de usá-los como base do plano.

## Atalhos e resultados

| Atalho no chat | O que fornecer | Resultado esperado |
| --- | --- | --- |
| `/pdi-iniciar` | Dizer se já tem PDI; responder às perguntas faltantes | Contexto recuperado, rascunho/proposta e próximo passo |
| `/pdi-status` | Ciclo, se quiser consultar um rascunho específico | Resumo de pendências, atrasos e próximo passo, sem alterar estado |
| `/pdi-importar` | Arquivo ou caminho do PDI/avaliação | Fonte preservada e proposta de incorporação |
| `/pdi-atualizar` | Relato, data e eventual evidência | Proposta com diferenças e registros após revisão |
| `/pdi-p2p` | Período e assuntos da conversa | Pauta em notas com avanços, dificuldades e perguntas |
| `/pdi-marco` | Período ou marco desejado | Consolidação em notas com realizações e evidências |
| `/pdi-exportar` | Ciclo e destino/formato desejado | Arquivos Markdown/JSON para revisar e copiar |
| `/pdi-fechar` | Ciclo a encerrar | Prévia de pendências; archive verificável após autorização |
| `/pdi-novo-ciclo` | Período e objetivos, mesmo incompletos | Novo rascunho, com ativação e transferências revisadas separadamente |

Os atalhos conduzem conversas; não são executáveis do terminal. O assistente informa o caminho de cada artefato criado e se está em rascunho, proposto ou aplicado.

## Pausar e retomar o início

O assistente registra respostas ainda incompletas em `pessoal/inbox/onboarding.md`, usando o [modelo de notas](../templates/onboarding.md), ou em propostas. Respostas aprovadas entram no perfil/calendário por `proposal` e `apply`. Uma nota ou proposta pendente não é um compromisso aplicado.

Em outra sessão, `/pdi-iniciar` consulta o estado, as propostas pendentes e essas notas antes de perguntar novamente. Se houver vários rascunhos, você escolhe qual retomar. Nenhum é ativado apenas por ser consultado. Informações que você ainda não conhece podem continuar pendentes; não é obrigatório anexar documentos para preparar o rascunho.

No terminal:

```bash
python3 scripts/pdi.py onboarding --format text
python3 scripts/pdi.py status --format text
python3 scripts/pdi.py onboarding --cycle ID_DO_RASCUNHO --format text
```

## Informações úteis

Avaliação anterior, feedbacks, matriz de competências, PDI parcial, P2Ps, retro, entregas, certificações e aspirações. Datas reais do ciclo, cortes, disponibilidade e restrições são essenciais. Pode começar sem todas as informações: desconhecidos ficam registrados. Evidência que só existe em link pode ser referenciada, mas não será chamada de inspecionada sem leitura.

## Receber um plano

Revisar prioridades, ações já assumidas, esforço, oportunidades e comprovação. Cada ação explica qual objetivo/competência apoia. O sistema prioriza requisitos que podem bloquear elegibilidade, mas não obriga cumprir todos os adicionais. Não aceite um plano que depende continuamente de ampliar a jornada.

Quando faltar estimar uma ação, o painel mostra esforço total pendente e a soma das estimativas já informadas. Isso ainda não permite afirmar que o plano cabe no tempo disponível. Se essa soma já ultrapassar sua capacidade, o alerta de sobrecarga aparece mesmo com outras estimativas pendentes. Zero horas representa uma estimativa explícita; deixe desconhecido o que você ainda não consegue estimar.

## Registrar novidade

Enviar arquivo, link ou relato e dizer o que aconteceu e quando. O assistente preserva a origem, associa a ações e apresenta alterações. Uma sugestão na P2P não é automaticamente um compromisso. Cancelar ou adiar uma ação oficial precisa de alinhamento; a história continua no sistema.

## Revisão mensal e trimestral

Pedir “Prepare minha P2P” ou “Prepare minha entrega parcial”. A P2P traz avanços, dificuldades e perguntas. A entrega parcial consolida realizações/evidências do período e prepara registros do PDI. Ações longas podem atravessar marcos. Não registrar o mesmo resultado como várias realizações.

## Team Guide

O assistente prepara título e descrição por ação. O export gera Markdown e JSON com tamanho verificado. Revisar e copiar manualmente. Informar depois se o registro foi realizado, com identificação externa quando disponível. O arquivo local sozinho não comprova preenchimento do Team Guide.

## Quando outro ciclo começa

Solicitar fechamento, revisar pendências e arquivar. Informar novas datas, avaliação e mudanças de função ou regras. O ciclo antigo permanece preservado. Uma evidência histórica pode ser válida para nova janela, mas não vira realização nova. Ações incompletas só são transferidas deliberadamente e não desaparecem da análise anterior.

## Compartilhar com gestor

Solicitar resumo específico, removendo informações que não deseja compartilhar. O produto não disponibiliza seus arquivos automaticamente. A interpretação das regras e seu enquadramento devem ser alinhados com a liderança.

## Sinais de erro

Se o assistente não conseguir dizer a revisão/ciclo atual, interromper mudanças e conferir o ambiente. Se afirmar promoção garantida, box oficial inferido ou regra não documentada, pedir a fonte e corrigir. Se houver proposta stale, hash divergente ou edição manual, seguir troubleshooting. Não editar arquivos internos para contornar erro.
