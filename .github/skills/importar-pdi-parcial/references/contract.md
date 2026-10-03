# Contrato específico

**Ativa quando:** há PDI existente ou histórico de ações. **Entradas:** exportação, calendário e critérios. **Passos:** guardar baseline; extrair ações e identificadores; detectar duplicatas; preservar títulos, estados, prazos e links; pedir data real quando necessária; associar ações ao ciclo; mostrar proposta de melhoria. **Saídas:** ações importadas e relatório de diferenças. **Aceitação:** registros já concluídos permanecem e tarefas futuras não viram realizadas. **Limite:** não adivinha campos externos ausentes ou reescreve diretamente o Team Guide.

## Operação local

Importar fonte com `import`; criar operações upsert em actions e objectives. Preservar título/prazo/status e `external_id` se conhecido. Enviar ao fluxo proposal/apply; não converter MD diretamente em fatos confirmados.

As verificações semânticas dependem do assistente e da revisão humana; o CLI protege estrutura e persistência.
