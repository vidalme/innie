---
name: pdi-status
description: "Consultar contexto, pendências e próximo passo sem alterar o estado."
agent: copiloto-desenvolvimento
---

Seguir o [contrato geral](../../AGENTS.md) e a [skill onboarding-e-retomada](../skills/onboarding-e-retomada/SKILL.md). Recuperar o estado canônico antes de conduzir o pedido.

Executar status; usar --cycle ID se o usuário escolheu um rascunho. Sem ciclo ativo, mostrar rascunhos e orientação. Entregar na conversa revisão/ciclo, calendário, atrasos, evidências faltantes e próxima ação; distinguir esforço desconhecido de zero. Não criar ciclos, propostas, notas ou renderizações nesta consulta.

Se faltar capacidade de execução/leitura, declarar o bloqueio e fornecer a próxima ação concreta; não afirmar criação, leitura ou aplicação não realizada.
