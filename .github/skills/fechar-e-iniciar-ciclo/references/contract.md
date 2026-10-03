# Contrato específico

**Ativa quando:** fechamento ou solicitação de novo ciclo. **Entradas:** ciclo atual, resultado disponível, calendário novo e objetivos selecionados. **Passos:** consolidar; revisar pendências; gerar arquivo verificável; registrar fechamento; criar novo rascunho; selecionar transferências e reavaliar janelas. **Saídas:** archive rotulado, novo ciclo e relatório de transferência. **Aceitação:** ciclo antigo íntegro, percentuais não herdados e evidências históricas identificadas. **Limite:** não sobrescreve arquivo existente; resultados tardios entram como adendo.

## Operação local

Revisar `status`, render e evidências; executar `cycle close ID --approve` após decisão; verificar archive; criar novo ciclo com `cycle create`, revisar datas e `cycle start --reviewed`. Transferir ações incompletas com `cycle carry`, sem limpar pendências anteriores.

As verificações semânticas dependem do assistente e da revisão humana; o CLI protege estrutura e persistência.
