# Auditoria de prontidão para um segundo usuário

Data: 03/10/2026, America/Fortaleza. Núcleo analisado: `75a4a4d`, versão 0.1.0.

## Parecer

O Innie já possui um núcleo funcional de persistência, revisão e exportação. Clonar e rodar o bootstrap funciona em Linux nas condições testadas. O que ainda não está pronto é a experiência autônoma de uma pessoa que desconhece a conversa de origem: descobrir o próximo passo, fornecer apenas o necessário, retomar um onboarding incompleto e receber resultados consistentes.

Minha avaliação: adequado a um piloto acompanhado; ainda precisa dos ajustes prioritários abaixo para um piloto por autoatendimento. Isso é um parecer técnico sobre o repositório, não uma avaliação institucional.

**Andamento em 03/10/2026:** A03 foi corrigido após esta auditoria. O setup agora confere o destino antes de inicializar o estado individual. Dois testes de regressão foram acrescentados; a suíte passou com 50 testes. Os resultados de 48 testes e a falha reproduzida abaixo registram a situação anterior à correção.

**Etapa seguinte — A04:** implementada a conexão explícita para um estado existente sem vínculo. O comando mostra o destino e orienta `--outtie CAMINHO connect` ou a criação em outra pasta. Setup repetido reconhece vínculos pelo symlink ou configuração local; consultas sem vínculo também deixam de assumir a pasta irmã preenchida. A reprodução com duas instalações vizinhas está coberta por teste de bootstrap em subprocessos.

Validação de A04: 55 testes passaram; `check_package.py` e `git diff --check` passaram. As novas fixtures são sintéticas e não alteram o outtie do participante.

Para dois participantes, a arquitetura local é suficiente: cada pessoa usa seu clone e seu outtie. Não há necessidade demonstrada de servidor, contas centralizadas, banco compartilhado ou mais agentes. O esforço principal deve ir para a jornada, a confiabilidade da preparação e os testes de uso.

## Escopo e evidências

A revisão cobriu instalação e aquisição, toda a implementação Python, wrappers, armazenamento, schemas, testes, CI, agentes, prompts, skills, templates, contratos, documentação atual e planejamento histórico. O pacote institucional foi examinado quanto a configuração, caminhos, proveniência e dependências dos anexos originais. Não houve revalidação externa das regras ou auditoria visual de todas as imagens/fontes institucionais.

Foram executados:

| Verificação | Resultado observado |
| --- | --- |
| `doctor` e `state` da instalação atual | Diagnóstico aprovado; revisão 0, sem ciclo nem fontes; nenhuma alteração canônica pessoal |
| `python3 -m unittest discover -s tests -v` | 48 testes passaram em Linux/Python 3.12.3 |
| `python3 scripts/check_package.py` | Passou |
| `check_package.py --distribution` em extração limpa de `git archive HEAD` | Passou |
| Dois clones Git locais, em pastas pai separadas, seguidos de bootstrap e doctor | Passaram; outties distintos e árvores Git limpas |
| Repetição do bootstrap | Preservou o estado |
| Ciclo sintético → proposta → aplicação → plano/painel → exportação → backup → restauração | Passou |
| Primeiro status sem ciclo e com apenas um rascunho | Falhou com `Ciclo não encontrado: None` |
| Setup com destino dentro do núcleo | Recusou a conexão, mas já havia criado o estado no destino inválido |
| Novo clone na mesma pasta pai de outro | Reutilizou o outtie existente sem confirmação de identidade |
| Ação planejada sem esforço informado | Apareceu como 0 horas; com capacidade configurada, `over_capacity` foi false |
| Skill deliberadamente invalidada em cópia temporária | `check_package.py` continuou aprovando |

Os testes novos usaram apenas pessoas e ações fictícias em diretórios temporários. O teste de clone foi local: autenticação, permissões e aquisição via GitHub não foram ensaiadas. Windows/WSL2 real, descoberta das customizações no VS Code e qualidade das respostas do Copilot permanecem sem validação nesta auditoria.

O sandbox desta sessão falhou antes de executar comandos por conflito entre o symlink `pessoal` e a proteção de `pessoal/.git`. A inspeção prosseguiu por execução local autorizada. Isso é uma observação deste ambiente, não prova de falha geral no VS Code. O teste de duas raízes descrito em [troubleshooting](../troubleshooting.md) continua necessário no ambiente do participante: abrir o workspace local, pedir revisão/ciclo e comparar com `state`. Esse teste não garante, por si só, resolver a política de sandbox de outro aplicativo.

## O que já está suficientemente estruturado

- Separação física entre conhecimento compartilhado e contexto individual, com configuração local ignorada pelo Git.
- CLI sem dependências de pip e bootstrap idempotente no caminho normal.
- Revisões com hash, lock, publicação atômica e rejeição de propostas desatualizadas.
- Preservação de fontes, deduplicação por conteúdo e distinção entre relato e confirmação.
- Proteção contra sobrescrita silenciosa de visões editadas manualmente.
- Exportação por ação, limite UTF-16, backup/restauração e congelamento de ciclos.
- Contratos explícitos para autorização e para não inventar promoção, critérios ou evidências.

Esses componentes devem ser preservados. A interface guiada pode utilizá-los sem reescrever o armazenamento.

## Achados prioritários antes do segundo usuário

As prioridades abaixo são desta auditoria: P1 = corrigir antes de anunciar autoatendimento; P2 = consolidar durante o piloto; P3 = evolução posterior. Não substituem as prioridades RF/RNF do planejamento histórico.

### A01 — P1: o bootstrap termina antes de começar a experiência

**Evidência:** [bootstrap.sh](../../scripts/bootstrap.sh) apenas encaminha para `setup`; [cli.py](../../src/pdi_copilot/cli.py), função `run`, inicializa e conecta. A saída contém `initialized`, `outtie`, `symlink` e `workspace`. Não há coleta de perfil, detecção de campos faltantes, resumo de prontidão ou próximo comando para a pessoa.

O `doctor` começa carregando o estado: antes de setup, termina com erro de leitura de metadata. Depois de setup, pode informar `ok: true` mesmo com `copilot_context: manual_check_required`. São estados diferentes que a experiência precisa explicar.

**Ajuste:** apresentar preparação concluída, destino individual, workspace a abrir, teste de integração pendente e `/pdi-iniciar`. Separar diagnóstico do ambiente de validação dos dados. Verificar versão mínima de Python e ferramentas antes de modificar a instalação, com instruções de recuperação compreensíveis.

**Aceite:** uma pessoa sai do bootstrap sabendo exatamente onde continuar; ausência de Python compatível, configuração ou autenticação tem encaminhamento explícito, sem declarar que o assistente já está pronto.

### A02 — P1: primeiro uso e retomada dependem de improvisação do modelo

**Evidência:** [onboarding-e-retomada](../../.github/skills/onboarding-e-retomada/SKILL.md) pede para confirmar perfil/calendário com perguntas curtas, mas não define sequência mínima, campos impeditivos, tratamento de interrupção ou entrega inicial. `status` e `render` falham quando não há ciclo ativo; mesmo um rascunho existente exige que alguém descubra seu ID e use `--cycle`.

**Ajuste:** definir estados de jornada derivados do contexto: instalação pendente, perfil incompleto, ciclo a escolher, calendário parcial, fontes a revisar e plano pronto para proposta. Permitir começar sem todos os documentos; perguntar somente o que impede o próximo resultado. Recuperar respostas persistidas em proposta aplicada ou rascunho na inbox, distinguindo o que foi aprovado. Exibir e retomar rascunhos existentes antes de sugerir outro ciclo.

**Aceite:** interromper após duas respostas e abrir outra conversa retoma o ponto correto; `status` sempre orienta, inclusive quando ainda não há plano. Não introduzir campos canônicos novos sem observar a política de versão/migração.

### A03 — P1: setup valida o destino depois de gravar nele

**Evidência reproduzida:** em cópia descartável, `python3 scripts/pdi.py --outtie ./nested-private setup` devolveu erro porque innie e outtie não podem conter um ao outro, mas `nested-private/metadata.json` e revisões já existiam e a pasta aparecia no Git. Em [cli.py](../../src/pdi_copilot/cli.py), `store.initialize()` precede `connect()`, onde está a checagem de topologia.

A fixture começou vazia: não foi observado vazamento de dados pessoais reais. O problema é a criação de estrutura individual fora da localização admitida, apesar da falha anunciada.

**Ajuste:** validar caminhos, conflito com `pessoal`, troca de destino e condições Git antes de inicializar. Uma rejeição previsível deve ocorrer sem criar o estado. Tratar falhas intermediárias com recibo e recuperação explícita.

**Aceite:** destino aninhado, dentro de `.git`, igual ao núcleo, ou ligação conflitante são recusados antes de qualquer criação canônica; adicionar teste pela CLI de setup, além do teste existente de `connect`.

### A04 — P1: um clone novo pode assumir um contexto preexistente

**Evidência reproduzida:** [resolve](../../src/pdi_copilot/cli.py) usa `INNIE.parent / 'outtie'` na ausência de configuração. Dois clones irmãos acabaram conectados ao mesmo perfil fictício. `setup` validou e reutilizou esse estado sem perguntar a quem pertencia.

Isso não significa que computadores distintos compartilhem dados. A reprodução exige pasta pai comum e acesso ao mesmo filesystem. Ainda assim, afeta instalações de teste, demonstrações e máquinas compartilhadas.

**Ajuste:** no primeiro vínculo, distinguir criar de reconectar; mostrar o destino e confirmar a escolha de um espaço existente. Preservar a idempotência de instalações já vinculadas. Documentar uma pasta de instalação própria por pessoa.

**Aceite:** clone sem vínculo nunca assume silenciosamente um outtie existente; duas instalações independentes mantêm fontes, perfil e ciclos separados.

### A05 — P1: desconhecidos viram afirmações no plano

**Evidência:** [blank_state e blank_cycle](../../src/pdi_copilot/model.py) presumem DevOps, Operação, America/Fortaleza e ausência de liderança. Esses padrões são compatíveis com o piloto descrito, mas não representam respostas de cada pessoa. O ciclo copia `evidence_cutoff_on` para `pdi_closes_on`, embora [os contratos](../data-contracts.md) tratem esses marcos separadamente.

Também foi reproduzido que esforço ausente vira zero em [overview/render](../../src/pdi_copilot/views.py). Com capacidade de duas horas semanais, uma ação sem estimativa resultou em `estimated_remaining_effort_hours: 0` e `over_capacity: false`. Enviar `effort_hours: null` foi rejeitado pelo validador.

**Ajuste:** apresentar padrões como sugestões a confirmar; manter fechamento do PDI desconhecido até informação própria; aceitar e exibir esforço desconhecido, com soma parcial e aviso de estimativas faltantes. Não concluir que o plano cabe na capacidade enquanto faltarem estimativas necessárias.

**Aceite:** nenhum dado desconhecido vira uma decisão implícita sobre a pessoa, o calendário ou a viabilidade do plano.

### A06 — P1: os atalhos têm nomes distintos, mas contratos pouco distintos

**Evidência:** os nove [prompts](../../.github/prompts) repetem praticamente o mesmo corpo, trocando a skill referenciada. `/pdi-status` aponta para onboarding; `/pdi-fechar` e `/pdi-novo-ciclo` apontam para o mesmo fluxo composto. As skills ajudam, mas não garantem fronteiras nítidas entre consultar, fechar e iniciar.

Faltam, na entrada de cada fluxo, parâmetros esperados, comportamento com informação insuficiente, saída concreta, local de gravação e critério de conclusão. P2P, diagnóstico e marco dependem de redação pelo modelo; `render` gera plano, painel e estado, sem executar esses outros produtos.

**Ajuste:** preservar os atalhos, especializando seus contratos. Status deve consultar e orientar; fechar deve concluir o fechamento solicitado; novo ciclo deve detectar ciclo ativo/rascunhos e conduzir a escolha. A aprovação autoriza mudanças concretas apresentadas, não uma sequência indefinida de transições. Padronizar nome/local/revisão dos artefatos e devolver links para abri-los.

**Aceite:** cada comando informa o que recebeu, o que falta, qual produto entregou e onde ele está; não exige que a pessoa selecione especialistas ou escreva operações JSON.

### A07 — P1: a distribuição ainda fala com quem recebeu os anexos no browser

**Evidência:** [README](../../README.md) e [INSTALL](../../INSTALL.md) começam pela extração de ZIP e por duas pastas entregues juntas. Git aparece no fim do guia. [Manutenção](../maintenance.md) ainda ensina o primeiro commit e a criação do remoto. O [planejamento histórico](../planning/README.md) identifica o piloto por nome e afirma não haver scripts implementados; está sinalizado como histórico na documentação principal, mas pode confundir uma leitura isolada.

A dependência dos anexos também aparece no conhecimento ativo: [summary.md](../../knowledge/policies/summary.md) cita I08 e X02; [requirements.md](../../knowledge/evidence-guidance/requirements.md) cita P01. Esses IDs não estão no [registro distribuído](../../knowledge/sources/registry.json). Não se deve resolver isso publicando os documentos pessoais originais. Os arquivos I01–I06 existem e seus hashes conferem; I07 usa um caminho com base diferente dos demais (`../competencies/devops.json`).

**Ajuste:** colocar clone → bootstrap → abrir workspace → iniciar no começo; deixar importação de ZIP como alternativa. Separar contribuição/manutenção do uso cotidiano. Preservar o histórico com aviso local claro. Tornar a proveniência autocontida: registrar extratos institucionais sanitizados, fontes não distribuídas e suas limitações, normalizar caminhos e validar referências. A meta de valorização deve ser escolhida pela pessoa; “dois steps” pode continuar como objetivo do piloto, não como objetivo pessoal presumido.

**Aceite:** um novo participante entende e inspeciona a origem do que é utilizável, identifica o que permanece pendente e não precisa recuperar os 15 anexos da conversa original. O destino Git deve respeitar o caráter institucional privado já documentado.

## Consolidação durante o piloto

| ID | Prioridade | Achado e consequência | Ajuste proposto |
| --- | --- | --- | --- |
| A08 | P1 para anunciar compatibilidade | Integração real não ensaiada; arquivos em `.github` não comprovam descoberta no aplicativo. Padrão `pessoal/**` pode não corresponder à segunda raiz. O problema de sandbox desta sessão confirma a necessidade de teste por ambiente. | Declarar um ambiente de referência, registrar versões e executar roteiro real de descoberta, leitura, proposta e retomada. Outros ambientes ficam como não validados. |
| A09 | P2 | A política padrão é fixada em `blank_cycle`; `criteria` lê o catálogo corrente sem selecionar pela versão do ciclo; fechamento copia o knowledge presente naquele momento. Atualizar o núcleo pode deixar versão declarada e conteúdo utilizado divergentes. | No piloto, detectar divergência e pedir revisão explícita; posteriormente manter versões selecionáveis. Não reescrever archives. |
| A10 | P2 | `check_package.py` conta arquivos, lê JSON e verifica links; não valida o frontmatter alegado pela documentação. Um SKILL.md inválido passou no ensaio. CI usa Python 3.11/Ubuntu e não executa o modo de distribuição. | Validar os contratos efetivos das customizações, paths e IDs de fontes; testar pacote limpo e jornadas de primeiro uso em subprocessos. Atualizar o resultado documentado de 44 para evidência atual de 48 testes, sem confundir quantidade com cobertura. |
| A11 | P2 | Wrapper de instalação posiciona todas as opções antes de `setup`: `install.sh --no-two-roots` falhou. `bootstrap.sh --outtie CAMINHO` sem `setup` também falhou, conforme seu repasse atual. | Definir uma interface única e documentar opções por comando; adicionar testes dos exemplos que serão oferecidos ao usuário. O segundo caso é lacuna de ergonomia, não violação do contrato atual do wrapper. |
| A12 | P2 | Validação aceita `role: 123` e `leadership: 'false'`; `milestones: [1]` causa TypeError, fora das exceções tratadas na CLI. IDs de critérios inexistentes também passam; sua interpretação é atualmente delegada ao assistente. | Validar tipos e emitir erros por campo; verificar IDs contra o catálogo selecionado sem confundir validação estrutural com julgamento institucional. Harmonizar schemas e runtime. |
| A13 | P2 | Import extrai alguns formatos e preserva imagens/PDFs sem texto, mas não entrega uma fila de entradas aguardando leitura/associação. Relatos e URLs dependem de propostas manuais do assistente. | Exibir fontes importadas, extração disponível, revisão pendente e próximo passo. Distinguir importado, analisado, proposto e aplicado sem duplicar a fonte canônica. |
| A14 | P2 | `state` imprime todo o histórico; não há comando de contexto resumido ou lista amigável de ciclos/propostas. Falta uma visão das pendências do onboarding e de revisão. | Derivar resumo da revisão, ciclos, propostas e informações faltantes; manter saída estruturada para automação e legível para a pessoa. |
| A15 | P2 | Atualização é backup + Git + doctor; migrate só reconhece schema 1. Não há demonstração automatizada de atualização de versão preservando uma instalação preenchida. | Definir versão suportada, rotina de upgrade e recuperação; testar atualização em cópia sintética preenchida antes de distribuir mudança incompatível. |
| A16 | P2 | Backup pode produzir arquivo cujo conteúdo descomprimido ultrapasse o limite de 512 MiB aceito por restore; o limite está documentado, mas não é antecipado na criação. | Antecipar limites e verificar restaurabilidade. Orientar destino de backup fora da instalação e testar restauração antes de depender dele. |
| A17 | P3 | Há apenas a matriz DevOps e seleção de regras limitada à área; Linux/POSIX aparece na implementação via fcntl e Bash. | Assumir explicitamente o piloto DevOps no ambiente testado; acrescentar matrizes/plataformas conforme demanda real, sem anunciar generalidade antes da implementação. |

## Jornada proposta para o participante

Esta é uma proposta de experiência; novos comportamentos abaixo ainda não foram implementados.

1. **Clonar:** o README oferece um caminho principal de instalação por Git, requisitos e pasta própria. Usar a URL real do repositório autorizado, sem distribuir outtie preenchido.
2. **Preparar:** bootstrap verifica pré-requisitos, diferencia espaço novo de existente, prepara o workspace e explica o teste pendente do assistente.
3. **Começar:** `/pdi-iniciar` recupera o estado. Pergunta se há PDI/rascunho existente antes de criar ciclo; coleta perfil e objetivo em grupos curtos, confirmando os padrões do piloto.
4. **Fornecer entradas:** pedir um documento ou relato por vez, explicando o resultado que ele permite produzir. Datas desconhecidas permanecem desconhecidas e permitem rascunho.
5. **Receber proposta:** entregar diagnóstico breve, prioridades e plano candidato, com fontes, pendências, capacidade e diferenças frente ao PDI anterior.
6. **Revisar e aplicar:** apresentar mudanças materiais; aplicar pela CLI após autorização aplicável; devolver links para plano, painel e exportações.
7. **Retomar:** `/pdi-status` mostra contexto, próximos passos e lacunas, incluindo propostas ainda pendentes. Uma conversa nova funciona sem recapitulação manual.

| Entrada já existente | Informação mínima a solicitar | Entrega esperada |
| --- | --- | --- |
| `/pdi-iniciar` | Existência de plano, perfil, objetivo, capacidade e calendário conforme necessários | Contexto recuperável e proposta inicial ou próximo passo explícito |
| `/pdi-importar` | Arquivo/relato e ciclo de destino | Original preservado, extração/revisão e diferenças propostas |
| `/pdi-atualizar` | O que ocorreu, quando e origem | Novidade relacionada ao plano e alterações propostas |
| `/pdi-status` | Nada se o contexto já for suficiente | Progresso, atrasos, desconhecidos e próxima ação |
| `/pdi-p2p` | Data/contexto da conversa quando faltarem | Pauta curta persistida; depois, decisões separadas de sugestões |
| `/pdi-marco` | Período de referência | Resumo das realizações, evidências e pendências daquele período |
| `/pdi-exportar` | Ação ou conjunto selecionado | Texto revisável, arquivos e contagem; registro externo permanece separado |
| `/pdi-fechar` | Ciclo e decisão de encerramento | Revisão de pendências, archive verificado e confirmação do fechamento |
| `/pdi-novo-ciclo` | Plano existente, calendário e transferências desejadas | Novo rascunho revisável, preservando a história anterior |

A CLI existente pode continuar como infraestrutura. Não é necessário transformar cada operação interna em pergunta de terminal. Se o produto pretendido passar a ser independente do Copilot, haverá um escopo adicional: formulários ou outra interface, além de uma integração de inferência para a parte interpretativa. Esse não é um requisito demonstrado para o piloto atual.

## Ordem recomendada de implementação

1. **Corrigir efeitos e afirmações indevidos:** A03–A05, com regressões significativas para destinos inválidos, reconexão e dados desconhecidos.
2. **Fechar a entrada pelo Git:** A01 e A07; bootstrap com encaminhamento claro, guia curto e fontes autocontidas. Validar A08 no ambiente que será oferecido ao colega.
3. **Implementar a jornada guiada:** A02 e A06; estados derivados, perguntas mínimas, retomada e contratos de saída para os atalhos.
4. **Consolidar operação e distribuição:** A09–A16 conforme os cenários exercitados pelo piloto, priorizando política, validação e restauração.
5. **Ampliar suporte após evidência de uso:** A17 e outras integrações conforme necessidade.

Não há estimativa de prazo nesta análise: faltam capacidade de manutenção e definição do ambiente efetivo do colega. As etapas são entregas verificáveis e podem orientar pequenas mudanças separadas.

## Critério para dizer “pronto para o colega clonar e usar”

O colega, usando apenas o README e as mensagens do produto, deve conseguir clonar, preparar, verificar o contexto, responder ao onboarding, fornecer uma entrada, revisar uma proposta e abrir seu primeiro resultado. Depois deve conseguir fechar a conversa, retomar, atualizar uma ação, exportar e restaurar um backup sintético. Registrar intervenções do criador: cada intervenção necessária indica uma lacuna da jornada.

A validação deve incluir espaço existente, datas desconhecidas, ausência de documento, entrada sem extração e proposta pendente. Instalação já configurada deve continuar idempotente; instalação nova não pode assumir a identidade de um espaço vizinho. Uma exportação útil e uma retomada correta são evidências de prontidão mais relevantes que o número de agentes ou skills empacotados.

Esta auditoria adiciona somente este relatório ao núcleo. Não implementa os ajustes, não publica o repositório e não altera o estado pessoal canônico.
