---
name: fechar-e-iniciar-ciclo
description: "Fechar e iniciar ciclo. Usar para fechamento ou solicitação de novo ciclo."
---

# Fechar e iniciar ciclo

## Procedimento

1. Ler o [contrato de execução](references/contract.md) e as referências pertinentes; recuperar a versão vigente com `state`.
2. Identificar se o pedido é fechar ou criar outro ciclo. Para fechar: revisar status, render e evidências, mostrar pendências; executar `cycle close ID --approve` após autorização e verificar archive. Encerrar aqui se não houve pedido de novo ciclo.
3. Para novo ciclo: consultar rascunhos antes de criar com `cycle create`. Datas desconhecidas podem ficar no rascunho. Não fechar automaticamente o ativo. Revisar calendário e plano antes de `cycle start --reviewed`; um ativo anterior precisa de uma decisão de fechamento separada. Transferir ações incompletas com `cycle carry` apenas quando selecionadas e autorizadas, preservando pendências anteriores.
4. Separar fatos, relatos, decisões e inferências. Vincular cada afirmação relevante à fonte e ao ciclo.
5. Devolver diagnóstico/proposta conforme [formato de propostas](../../../docs/proposals.md). Não escrever diretamente em `revisions` ou `metadata.json`.
6. Resumir o que foi feito, o que permanece desconhecido e o próximo passo.

## Contratos e referências

- [Procedimento específico](references/contract.md): ler antes de executar esta skill.
- [Contratos de dados](../../../docs/data-contracts.md): ler ao criar operações.
- [CLI e scripts](../../../docs/scripts.md): conferir argumentos antes de executar.
- [Índice institucional](../../../knowledge/index.json): consultar regras quando a tarefa depender delas.

Não aplicar mudanças materiais sem revisão; não inventar evidências nem decisão do gestor; não assumir regra de 12 meses entre promoções. Se ferramenta, fonte ou data faltar, registrar a limitação e continuar apenas no que estiver fundamentado.
