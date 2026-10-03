# Contrato específico

**Ativa quando:** novidade altera o contexto. **Entradas:** evento processado, versão atual e critérios. **Passos:** detectar duplicidade; localizar impacto; propor mudanças mínimas; explicar custo e dependências; preservar anteriores; pedir revisão material; acionar aplicação. **Saídas:** proposta, histórico e visões regeneradas. **Aceitação:** duas submissões do mesmo evento não duplicam resultados; realizações não desaparecem. **Limite:** cancela/replaneja ações oficiais somente com decisão identificada; não aplica se a versão atual mudou.

## Operação local

Ler revisão atual; criar mudanças em JSON dentro de `pessoal/inbox/`; executar `proposal --changes CAMINHO --reason MOTIVO`. Mostrar diferenças e aplicar com `apply --proposal CAMINHO --approve` somente após revisão pertinente. Depois `render`.

As verificações semânticas dependem do assistente e da revisão humana; o CLI protege estrutura e persistência.
