# Contrato específico

**Ativa quando:** antes de aplicar plano material, exportar PDI ou fechar ciclo. **Entradas:** proposta e referências. **Passos:** validar fonte, prazo, capacidade, estado, autoria, janelas, critérios e redação; executar validadores determinísticos pertinentes. **Saídas:** parecer com erros e ajustes. **Aceitação:** falha bloqueante impede aplicação; incerteza institucional aparece explicitamente. **Limite:** um escore qualitativo opcional é avaliação do artefato, não chance de promoção.

## Operação local

Executar `validate`, `status`, `window` quando aplicável; revisar fontes, alterações materiais, datas e capacidade. Devolver pass/needs_revision/blocked com razões. Não transformar o parecer em aprovação institucional.

As verificações semânticas dependem do assistente e da revisão humana; o CLI protege estrutura e persistência.
