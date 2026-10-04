# Contrato específico

**Ativa quando:** começar, retomar ou consultar o contexto individual. Conexão de espaço existente segue INSTALL, com destino explícito.

**Entradas:** `state`, `onboarding`, pedido atual e, quando retornados, notas e propostas persistidas. Usar `--cycle ID` somente para a escolha explícita do usuário. Sem ferramentas, ler metadata e revisão indicada e declarar quais verificações não foram executadas.

**Saída de início/retomada:** resumo com revisão, ciclo escolhido, informações conhecidas/desconhecidas, fontes e propostas; respostas candidatas em inbox/onboarding.md ou proposta; próximo resultado combinado. Para perfil, `career_goal` pode guardar objetivo descritivo; objetivos do ciclo existentes também respondem a essa pergunta.

**Saída de status:** resposta na conversa com indicadores e orientação. Consulta não escreve estado, notas, propostas ou visões. Sem ciclo ativo, mostrar rascunhos/pendências e orientar a escolha, sem assumir que um rascunho é ativo.

**Aceitação:** outra sessão recupera respostas sem repetir perguntas já respondidas; uma proposta pendente não vira fato; múltiplos rascunhos não são selecionados automaticamente; ausência de documentos não impede plano provisório. Informações desconhecidas/adiadas permanecem visíveis, sem obrigar um questionário completo.

**Limites:** não migrar estado incompatível neste fluxo; não criar ciclo duplicado; não usar aprovação de uma resposta como autorização para compromissos novos. O terminal deriva orientação do estado; a conversa interpreta e registra respostas. Testes da CLI não demonstram a qualidade ou descoberta do assistente no editor.
