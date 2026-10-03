---
name: planejar-ciclo
description: "Planejar ciclo. Usar para plano inicial ou revisão material."
---

# Planejar ciclo

## Procedimento

1. Ler o [contrato de execução](references/contract.md) e as referências pertinentes; recuperar a versão vigente com `state`.
2. Confirmar datas. Usar `cycle create` para rascunho, calendário revisado via proposal; `cycle start ID --reviewed` somente após revisão. Usar objectives/actions/metrics, `effort_hours` como esforço restante estimado e `weekly_capacity_hours` no perfil.
3. Separar fatos, relatos, decisões e inferências. Vincular cada afirmação relevante à fonte e ao ciclo.
4. Devolver diagnóstico/proposta conforme [formato de propostas](../../../docs/proposals.md). Não escrever diretamente em `revisions` ou `metadata.json`.
5. Resumir o que foi feito, o que permanece desconhecido e o próximo passo.

## Contratos e referências

- [Procedimento específico](references/contract.md): ler antes de executar esta skill.
- [Contratos de dados](../../../docs/data-contracts.md): ler ao criar operações.
- [CLI e scripts](../../../docs/scripts.md): conferir argumentos antes de executar.
- [Índice institucional](../../../knowledge/index.json): consultar regras quando a tarefa depender delas.

Não aplicar mudanças materiais sem revisão; não inventar evidências nem decisão do gestor; não assumir regra de 12 meses entre promoções. Se ferramenta, fonte ou data faltar, registrar a limitação e continuar apenas no que estiver fundamentado.
