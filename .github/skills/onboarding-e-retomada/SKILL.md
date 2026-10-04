---
name: onboarding-e-retomada
description: "Onboarding e retomada. Usar para começar, continuar ou conectar um estado anterior."
---

# Onboarding e retomada

## Procedimento

1. Ler o [contrato de execução](references/contract.md). Executar `doctor` na primeira sessão ou após mudança da instalação; recuperar `state` e `onboarding`. Se faltar instalação, orientar bootstrap; se houver falha de integridade, seguir recuperação antes de escrever.
2. Para pedido de status, executar `status` (com `--cycle ID` quando escolhido), resumir contexto, pendências e próximo passo. Encerrar a consulta sem criar notas, propostas ou ciclos.
3. Para iniciar/retomar, ler os caminhos `resume_notes` e `pending_proposals` retornados por `onboarding`. Conferir revisão, respostas aplicadas e decisões anteriores antes de perguntar. Proposta desatualizada exige comparação com o estado atual; nota é candidata, nunca fato aplicado.
4. Sem ciclo ativo, apresentar rascunhos e pedir qual retomar. Sem rascunhos, perguntar se já existe PDI; importar se houver. Criar um rascunho somente quando essa intenção estiver estabelecida. Não presumir período, função, objetivo de promoção ou atuação em liderança.
5. Fazer no máximo duas perguntas por rodada, priorizando o necessário ao próximo resultado: objetivo/compromissos, função/nível/área, capacidade e calendário. Aceitar desconhecidos. Documentos são opcionais e o plano provisório pode avançar com lacunas explícitas; não insistir em perguntas adiadas.
6. Persistir respostas candidatas em `pessoal/inbox/onboarding.md` conforme o [modelo](../../../templates/onboarding.md), preservando origem e histórico, ou preparar uma proposta. Expor as diferenças materiais e aplicar somente após autorização aplicável. Não editar revisions/metadata. Atualizar a nota com a proposta aplicada, recusada ou substituída.
7. Consultar novamente a orientação depois de aplicar. Entregar resumo do contexto, caminho das notas/proposta/visão existente, lacunas e uma próxima ação. Quando o rascunho estiver pronto, revisar calendário e plano antes de ativar e renderizar.

## Contratos e referências

- [Procedimento específico](references/contract.md): ler antes de executar esta skill.
- [Contratos de dados](../../../docs/data-contracts.md): ler ao criar operações.
- [CLI e scripts](../../../docs/scripts.md): conferir argumentos antes de executar.
- [Índice institucional](../../../knowledge/index.json): consultar regras quando a tarefa depender delas.

Não aplicar mudanças materiais sem revisão; não inventar evidências nem decisão do gestor; não assumir regra de 12 meses entre promoções. Se ferramenta, fonte ou data faltar, registrar a limitação e continuar apenas no que estiver fundamentado.
