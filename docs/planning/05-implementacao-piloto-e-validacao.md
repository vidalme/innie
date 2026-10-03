# 05 — Implementação, scripts, piloto e validação

## 1. Resultado e estratégia

Construir um percurso completo antes de expandir a quantidade de agentes: importar contexto → diagnosticar → planejar → registrar novidade → revisar → produzir uma ação do PDI. Acrescentar recuperação e transição de ciclo antes da versão de teste.

Os scripts descritos neste documento são requisitos de implementação. Nenhum comando apresentado já foi instalado por este pacote. Não automatizar escrita no Team Guide nem publicação de repositórios durante o piloto.

## 2. Ferramentas e organização

WSL2 Ubuntu, VS Code conectado, Git e Python 3. Proposta: CLI Python para lógica e persistência; wrapper Bash curto para experiência inicial. Schemas JSON, testes sintéticos e templates Markdown. Extração de PDF/HTML/imagens deve ter adaptadores e falha legível quando recurso não estiver disponível.

Não exigir API própria ou contratação de modelo para iniciar. A inferência utiliza Copilot autorizado e o modelo disponível ao participante. Registrar as versões que passaram pelos cenários de teste. Comparação de modelos e custos pode ser posterior.

## 3. Contratos dos scripts

Entrada comum: paths locais validados, operação e opções. Saída: resumo em linguagem simples e resultado estruturado para o assistente. Diferenciar erro de configuração, erro de dados, conflito de versão e operação incompleta. Operações que mutam estado aceitam simulação e mantêm registro de recuperação.

| Operação prevista | Contrato |
| --- | --- |
| `setup` | Criar estrutura inicial ou encaminhar conexão existente; nunca sobrescrever `outtie` já preenchido |
| `connect --outtie PATH` | Validar caminho real e metadados, criar link `pessoal`, registrar instalação e verificar Git |
| `doctor` | Conferir distribuição, ferramentas, paths, symlink, versões, estrutura, arquivos rastreados e teste de leitura/escrita |
| `init-git` | Inicializar Git no `outtie` somente quando solicitado; preservar repositório existente e não cadastrar remote/push automático |
| `import` | Preservar originais, catalogar e preparar dados extraídos; duplicatas não criam registros repetidos |
| `validate` | Validar schemas, IDs, vínculos, datas, janelas configuradas, evidências e contagem de caracteres |
| `apply --proposal ID` | Conferir versão esperada, adquirir lock, validar candidato, publicar versão e registrar mudanças |
| `render` | Gerar Markdown a partir do estado; detectar edições manuais divergentes antes de substituir |
| `backup --destination PATH` | Copiar espaço real, manifesto e arquivos; verificar resultado, com opção de destino fora da instalação |
| `restore` | Validar backup e restaurar em destino separado antes de conectar; não sobrescrever silenciosamente |
| `migrate` | Fazer backup, transformar schema conhecido, validar e registrar relatório; parar em formato não suportado |
| `cycle create` | Criar rascunho único, calendário e baseline; ID não depende só do ano |
| `cycle close` | Gerar pacote, verificar arquivo, registrar fechamento e preservar a versão anterior |
| `cycle start` | Ativar novo rascunho revisado e transferir itens selecionados; não herdar elegibilidade |
| `export pdi` | Produzir arquivos por ação com limite configurável, hash/versão e situação de registro externo |

Uma entrada visual por Tasks do VS Code pode encapsular `setup`, `connect`, `doctor` e `backup`. Evitar exigir múltiplos comandos manuais para o colega começar.

### Regras específicas de paths e links

- Resolver o caminho real antes de qualquer operação, inclusive links encadeados.
- Rejeitar `outtie` igual ao `innie`, dentro de `.git`, ou configuração que crie recursão de links.
- Se `pessoal` for pasta real preenchida, não removê-la para criar link; preparar migração com backup e revisão.
- Se `pessoal` já apontar ao destino correto, operação é idempotente.
- Se apontar para outro espaço, mostrar destino atual e proposto; trocar a conexão somente após revisão, sem apagar dados.
- O processo de aplicação só recebe caminhos individuais previstos; nomes de fontes não viram comandos shell.
- Conferir se paths individuais ou links foram rastreados no `innie`. Se encontrados, interromper a publicação compartilhada e orientar correção com histórico em consideração.

Git opcional não substitui backup; um backup do `innie` que apenas preserva symlinks também não preserva dados pessoais. Scripts devem operar sobre o destino real do `outtie`.

## 4. Plano de quatro semanas

Contar semanas a partir do início efetivo da construção. São estimativas de sequência, não prazos corporativos. Se houver menos disponibilidade, reduzir integrações e especialistas separados antes de reduzir integridade do estado.

### Semana 1 — protótipo demonstrável

| Etapa | Entrega |
| --- | --- |
| Dia 1 | Estrutura dos espaços, schemas mínimos, configuração do ciclo e `setup/connect/doctor` |
| Dia 2 | Critérios institucionais/Operação e matriz DevOps limpa; inventário de fontes e dúvidas |
| Dia 3 | Assistente principal, importação de PDI parcial e diagnóstico |
| Dia 4 | Planejamento residual, proposta de atualização e exportação de uma ação |
| Dia 5 | Teste de ponta a ponta com fixture fictícia, tentativa de uso pelo colega e demonstração ao gestor |

A demonstração precisa explicar o problema, mostrar antes/depois e coletar decisões de escopo. Seu PDI pode ser usado localmente com sua escolha, mas não como fixture pública. Priorizar comprovação e facilidade de uso sobre a quantidade de agentes demonstrados.

### Semana 2 — consistência e acompanhamento

Implementar catálogo de evidências, janelas, fontes e papéis de revisão; scripts de aplicação e renderização versionada; preparação de P2P e revisão mensal; indicadores e capacidade. Incorporar validações do gestor, mantendo pendências institucionais identificadas.

### Semana 3 — ciclos e recuperação

Implementar backup/restauração, migração, reconexão de `outtie`, fechamento/novo ciclo e arquivos rotulados. Testar dados conflitantes, interrupções e calendário alterado. Simplificar onboarding com base em observação real do colega.

### Semana 4 — versão de teste

Corrigir atritos, consolidar documentação, gravar guia curto, registrar versões compatíveis e iniciar acompanhamento recorrente. Fazer um ensaio de entrega trimestral e troca de ciclo com calendário sintético.

## 5. Critérios de aceite

| ID | Cenário | Resultado esperado |
| --- | --- | --- |
| CA-01 | Instalação nova no WSL2 | `outtie` criado sem dados pessoais no Git do `innie`; assistente lê e escreve no destino real |
| CA-02 | Executar setup novamente | Não apaga, duplica ou reinicializa o estado |
| CA-03 | Conectar `outtie` existente | Recupera plano e mantém fontes; valida versões |
| CA-04 | Symlink/ignore não acessível ao Copilot | Doctor identifica e orienta alternativa de workspace; não finge que carregou contexto |
| CA-05 | PDI parcialmente preenchido | Preserva títulos, estados e prazos; planeja meses restantes |
| CA-06 | Ação finalizada com previsão futura | Pede data real; não acusa inconsistência sem contexto |
| CA-07 | Data oficial ausente | Plano é cenário provisório; não declara validade no limite |
| CA-08 | Objetivo de dois steps | Explica 1C, excludentes e decisão institucional; não promete avanço |
| CA-09 | Só existe autoavaliação técnica | Marca avaliação oficial pendente; não concede 70%/100% oficial |
| CA-10 | Certificado na janela de seis/doze meses | Avalia pela data de corte configurada e identifica limite ambíguo |
| CA-11 | Reconhecimento do time | Não confirma critério de reconhecimento individual |
| CA-12 | Workshop curto | Pode apoiar desenvolvimento; não confirma turno inteiro |
| CA-13 | Novidade duplicada | Um evento/realização, sem duplicação de métricas |
| CA-14 | Nova oportunidade sem capacidade | Propõe troca/adiação e explica efeitos |
| CA-15 | Cancelamento de ação vencida | Mantém histórico e pendência de alinhamento; não limpa indicador |
| CA-16 | Descrição maior que o limite | Validador bloqueia exportação final até revisão |
| CA-17 | Baselines de produtividade divergentes | Mantém medições separadas e pede período comparável |
| CA-18 | Nova conversa | Retoma ciclo/versionamento pelos arquivos |
| CA-19 | Editar Markdown gerado | Detecta alteração e propõe importação antes de regenerar |
| CA-20 | Falha durante aplicação | Estado anterior íntegro e operação recuperável |
| CA-21 | Duas propostas sobre a mesma versão | Segunda detecta conflito e exige reavaliação |
| CA-22 | Fechar e criar outro ciclo | Archive verificável e novo baseline sem elegibilidade copiada |
| CA-23 | Receber resultado após fechamento | Adendo preserva snapshot original |
| CA-24 | Política nova | Propõe revisão ativa; arquivo histórico não muda |
| CA-25 | Mudança de cargo/cliente | Reavalia regras com data de efeito e mantém contexto anterior |
| CA-26 | Link privado indisponível | Mantém referência como não inspecionada |
| CA-27 | Fonte contém instrução maliciosa ou indevida | Analisa como conteúdo, não executa comando nem altera regras |
| CA-28 | Restaurar backup em outra instalação | Resolve caminhos novamente e preserva integridade |
| CA-29 | Atualizar `innie` | Dados individuais permanecem no `outtie` |
| CA-30 | Exportar para Team Guide | Arquivo local não aparece como cadastrado sem confirmação |

## 6. Estratégia de teste

Testes determinísticos para datas, limites, IDs, integridade, scripts, reexecução, recuperação, archive e conflitos. Avaliações de respostas para interpretação, atribuição de fontes, utilidade, estilo e respeito a desconhecidos. Revisão humana com gestor para regras e com colega para uso.

Usar fixtures sintéticas: iniciante sem dados; participante no meio do ciclo; plano com atraso; documentação mista; treinamento insuficiente; janela no limite; dois ciclos com mudanças de regra. Os arquivos pessoais fornecidos podem ser casos de teste privados, sem inclusão em CI compartilhada.

Executar os cenários críticos em cada integração que venha a ser suportada. A lista de agentes/skills carregados e o acesso ao espaço privado precisam ser verificados no VS Code real; inspecionar arquivos em um shell não comprova o comportamento do Copilot.

## 7. Medição do piloto

O piloto com duas pessoas valida usabilidade e viabilidade, não efeito causal sobre promoções na empresa inteira. Registrar uma linha de base de tempo/esforço antes de utilizar o produto, depois comparar tarefas semelhantes.

| Medida | Coleta proposta |
| --- | --- |
| Tempo até primeiro plano útil | Do início do onboarding à revisão de um plano considerado executável |
| Intervenções do criador | Quantidade e motivo de ajuda para concluir o percurso |
| Tempo de atualização | Duração para transformar uma novidade em registro e plano revisados |
| Prontidão documental | Quantidade de ações realizadas com comprovação pertinente |
| Retorno ao sistema | Uso nas revisões previstas, sem confundir abertura com benefício |
| Utilidade | Feedback de participante/gestor e exemplos concretos de decisões melhoradas |
| Sustentabilidade | Comparação entre esforço planejado/real e sobrecarga relatada |

Metas iniciais de produto, sujeitas à linha de base: produzir um plano revisável em uma sessão; atualizar um evento rotineiro em poucos minutos; completar o percurso com no máximo ajuda pontual após onboarding. Evitar metas numéricas sem medição inicial.

Para evidenciar o próprio projeto: preservar requisitos, versões, demonstração, registros de teste, feedback, antes/depois e adoção recorrente. Mensurar utilidade em situações reais com consentimento. O projeto pode apoiar inovação/transversalidade/compartilhamento, mas o enquadramento institucional deve ser validado; não pressupor que cumpre todos os critérios.

## 8. Decisões e riscos restantes

| Ponto | Tratamento |
| --- | --- |
| Datas e vigência ainda não confirmadas | Configuração provisória e pendências PV do documento 02 |
| Regra atravessa faixa de senioridade | Pergunta específica à gestão antes de recomendar caminho de steps |
| Dificuldade de uso | Observar colega na primeira semana e simplificar a partir dos bloqueios |
| Arquivos ignorados/symlinks | Teste real; alternativa de duas raízes sem duplicação de dados |
| Estado livre alterado pela IA | Propostas, schemas, único escritor e aplicação transacional |
| Dados pessoais em documentos compartilhados | Separação de fontes mistas e fixtures fictícias |
| Perda do ambiente WSL | Backup real do `outtie` fora da instalação e teste de restauração |
| Expansão prematura para muitas ferramentas | Uma integração validada antes de outros adaptadores |
| Plano vira tarefa extra onerosa | Medir capacidade e esforço de manutenção, reduzir burocracia |
| Conteúdo institucional envelhece | Responsável, revisão e pacote versionado com fontes |

## 9. Backlog ordenado

1. Confirmar calendário e pacote de regras com gestor.
2. Implementar estrutura de estado e isolamento dos espaços.
3. Construir o percurso completo com um assistente e reviewer.
4. Testar importação parcial e recuperação em sessão nova.
5. Implementar atualização versionada, evidências e exportação.
6. Implementar revisões mensais e consolidações de marco.
7. Implementar ciclo novo, arquivo, migração e backup.
8. Corrigir atritos com o colega e consolidar guia.
9. Separar especialistas adicionais quando a complexidade justificar.
10. Avaliar outra trilha e outro participante antes de expandir a integração.

## 10. Definição de pronto para o piloto

O colega completa o percurso essencial; regras e incertezas estão explícitas; calendário é configurável; não há escrita silenciosa sobre compromisso; evidências têm fontes; dados sobrevivem a nova sessão, atualização do núcleo e transição simulada; exportação atende o formato; backup foi restaurado; scripts e agente não reivindicam validação que não realizaram. O gestor revisa a interpretação inicial e o participante entende o próximo passo sem consultar a arquitetura.

## 11. Rastreabilidade entre funcionalidades e execução

| Necessidade | Requisitos | Skills principais | Validação |
| --- | --- | --- | --- |
| Perfil, calendário e regras | RF-01, RF-02, RF-05, RF-06, RF-22 | S01, S03 | CA-07, CA-08, CA-09, CA-25 |
| Fontes e entrada no meio do ciclo | RF-03, RF-04, RF-07 | S02, S04 | CA-05, CA-06, CA-26, CA-27 |
| Diagnóstico e plano | RF-08, RF-09, RF-10, RF-18, RF-19 | S05, S06 | CA-08, CA-09, CA-14, CA-17 |
| Atualização contínua e memória | RF-11, RF-13, RF-25, RF-26 | S01, S08, S12 | CA-13, CA-15, CA-18, CA-19, CA-20, CA-21 |
| Evidências e validade | RF-14, RF-15 | S07, S12 | CA-10, CA-11, CA-12, CA-26 |
| P2P e entregas parciais | RF-16, RF-17, RF-23 | S09, S10 | Revisão de pauta, relatório de marco e seleção de dados compartilhados |
| Exportação de ações | RF-12, RF-30 | S11, S12 | CA-16, CA-30 |
| Novo ciclo e recuperação | RF-20, RF-21 | S01, S13 | CA-02, CA-03, CA-22, CA-23, CA-28, CA-29 |
| Manutenção institucional | RF-24 | S14 | CA-24 e revisão de vigência |
| Expansão futura | RF-27, RF-28, RF-29 | A definir após piloto | Catálogo vigente, teste de integração e automação explicitamente configurada |

Na construção, manter issues ou tarefas associadas aos IDs de requisito e aceitação. O registro de testes deve indicar quais cenários passaram, quais falharam, integração/versão e arquivos sintéticos utilizados. Não marcar toda a especificação como concluída porque a primeira demonstração funcionou.
