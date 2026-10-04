---
name: pdi-importar
description: "Preservar uma fonte e propor sua incorporação ao plano."
agent: copiloto-desenvolvimento
---

Seguir o [contrato geral](../../AGENTS.md) e a [skill importar-pdi-parcial](../skills/importar-pdi-parcial/SKILL.md). Recuperar o estado canônico antes de conduzir o pedido.

Pedir arquivo/caminho se ausente e identificar ciclo desejado. Importar com import, preservando original e respeitando deduplicação. Se extração falhar, declarar leitura pendente. Separar ações já realizadas, compromissos e sugestões. Entregar ID/caminho da fonte e proposta de incorporação com conflitos/lacunas; não tratar importação como aprovação do plano.

Se faltar capacidade de execução/leitura, declarar o bloqueio e fornecer a próxima ação concreta; não afirmar criação, leitura ou aplicação não realizada.
