# Agentes, skills e instruções

## Catálogo

| Agente | Uso |
| --- | --- |
| copiloto-desenvolvimento | Interface única, memória, perguntas, revisão e aplicação |
| analista-desenvolvimento | Diagnóstico e diferenças entre avaliação oficial e inferência |
| planejador-desenvolvimento | Prioridades, capacidade, cronograma e entregas |
| curador-evidencias | Fonte, autoria, realização e validade |
| redator-pdi | Texto do PDI, resumos e pauta de conversa |
| revisor-consistencia | Fontes, plausibilidade, mudanças e pendências |
| mantenedor-institucional | Atualização do núcleo e das regras |

Somente copiloto e mantenedor aparecem no seletor por padrão. Especialistas são read-only e invocáveis pelo modelo conforme capacidades. Não há obrigação de invocar todos em cada sessão. No harness sem delegação, o copiloto executa os procedimentos das skills sequencialmente.

## Catorze skills

Onboarding e retomada; processar fontes; selecionar regras; importar PDI parcial; diagnosticar desenvolvimento; planejar ciclo; registrar evidências; atualizar plano; preparar P2P; consolidar marco; redigir PDI; revisar qualidade; fechar/iniciar ciclo; manter conhecimento.

Cada skill possui SKILL.md com name/description e uma referência de contrato específico. Os procedimentos apontam para a CLI real e os contratos de dados. Os detalhes de regras não estão duplicados nos prompts; vivem em knowledge. Para triggers e entradas/saídas completas, consultar a especificação em docs/planning/04-agentes-skills-e-fluxos.md e os arquivos da skill pertinente.

## Atalhos

pdi-iniciar, pdi-importar, pdi-atualizar, pdi-status, pdi-p2p, pdi-marco, pdi-exportar, pdi-fechar, pdi-novo-ciclo. São prompt files que direcionam ao mesmo copiloto. Linguagem natural deve ser suficiente.

## Manutenção

Mudar descrição se os triggers mudarem. Manter SKILL.md enxuto; detalhes específicos ficam em references. Verificar caminhos relativos, comandos e saída em caso de ferramentas ausentes. Não criar uma cópia das regras em cada agente. Atualizar exemplos e testes quando mudar schema/CLI. O check_package valida formato e referências, mas teste real de resposta continua necessário.

## Revisor

Classificar pass, needs_revision ou blocked com localização do problema e correção. Não usar score de resposta como chance de promoção. Limitar correções automáticas a duas rodadas e devolver dúvidas persistentes ao usuário. Mesmo modelo revisando sua própria resposta é uma limitação a declarar; um segundo papel não é automaticamente uma revisão independente.

## Segurança e expectativas

Instruções não são sandbox. Ferramentas read-only só limitam especialistas onde o harness respeita a configuração. O orquestrador usa ferramentas de escrita para notas/propostas e CLI; o usuário e o sistema de permissões da integração controlam execução. Não declarar que um prompt sozinho impede acesso ou publicação.
