# 01 — Produto, experiência e requisitos

## 1. Problema e proposta

Colaboradores precisam conectar informações dispersas: critérios institucionais, expectativas por senioridade, avaliações, feedbacks, aspirações, oportunidades e evidências de trabalho. Organizar isso somente no fechamento dificulta corrigir lacunas, cumprir prazos e demonstrar impacto.

O copiloto transforma essas entradas em decisões de desenvolvimento ao longo do ciclo. Seu encadeamento central é:

**Critério ou competência → objetivo → ação → entregas → resultado → evidências → registro no PDI.**

Nem todo objetivo pessoal corresponde a um critério de valorização. O sistema preserva objetivos de carreira de longo prazo e sinaliza quando uma atividade não possui relação institucional confirmada. Não apresenta todo curso ou projeto como requisito de promoção.

## 2. Objetivos e público

### Objetivos do produto

1. Tornar as regras compreensíveis e rastreáveis.
2. Priorizar lacunas que comprometam elegibilidade e desenvolvimento.
3. Planejar ações compatíveis com capacidade, prazos e oportunidades reais.
4. Reduzir esforço para capturar e organizar evidências.
5. Apoiar conversas mensais e a consolidação trimestral do PDI.
6. Manter continuidade entre sessões, versões e ciclos.
7. Demonstrar qualidade de uso e benefício para outras pessoas.

O objetivo de até dois steps é uma preferência do usuário e do piloto, não um resultado que o software possa conceder. O sistema organiza condições de preparação; posição 9box, normalização, orçamento e decisão institucional não são controlados pelo colaborador.

### Público

Primeiro: dois profissionais DevOps. Segundo: outros profissionais técnicos, com as matrizes de suas funções. Futuro: todas as áreas da empresa, inclusive pessoas que não utilizam IDEs. A estrutura deve permitir expansão, sem presumir que critérios da Operação se aplicam às demais áreas.

### Papéis

| Papel | Responsabilidade |
| --- | --- |
| Colaborador | Fornecer contexto, executar ações, revisar registros e escolher o que compartilhar |
| Gestor | Alinhar prioridades, validar interpretações e expectativas e acompanhar desenvolvimento |
| Mantenedor do núcleo | Atualizar conteúdo institucional e versões da integração |
| RH/P&C | Esclarecer vigência, exceções, cálculo e requisitos que não puderem ser confirmados |

O gestor não recebe acesso automático aos arquivos privados. Compartilhamento ocorre por uma saída selecionada pelo colaborador. Não haverá ranking de funcionários nem painel corporativo nominal no piloto.

## 3. Escopo de entrega

### Protótipo na primeira semana

- Ambiente `innie`/`outtie` funcional no WSL2.
- Uma trilha DevOps processada e fontes identificadas.
- Assistente principal com fluxos de início, diagnóstico, planejamento, atualização e exportação.
- Importação de um PDI parcial, preservando registros existentes.
- Demonstração de uma novidade alterando o plano sem apagar realizações.
- Calendário configurável e cálculo de tempo restante.
- Uma ação do Team Guide exportada e revisada.
- Verificação mínima de symlink, isolamento Git e integridade do estado.

### Piloto até a quarta semana

Inclui revisão de evidências e janelas, preparação de P2P, metas e indicadores simples, consolidação por marco, histórico, recuperação, arquivamento e novo ciclo, guia de uso e testes com o colega. O piloto terá a transição de ciclo simulada: não precisa esperar maio para testá-la.

### Evoluções posteriores

Outras trilhas, adaptadores para outras ferramentas, experiência web, catálogo institucional de oportunidades, integrações com calendários e fontes corporativas, lembretes recorrentes e análise agregada consentida. RAG, MCP e banco de dados não são pré-requisitos do primeiro produto. Só devem entrar quando resolverem uma limitação observada.

### Fora do escopo inicial

Escrita automática no Team Guide; coleta massiva de Jira, e-mails ou transcrições; automação de mensagens; previsão probabilística de promoção; cálculo de salário com base em tabelas incompletas; reprodução da heurística institucional desconhecida; inferência de resultados privados da matriz 9box.

## 4. Experiência de uso

O colaborador seleciona um único assistente. A conversa oferece uma próxima ação concreta e poucas perguntas por vez. Não exige conhecimento de agentes, skills, JSON ou Git.

### Jornada A — começar sem plano

O assistente confirma função, senioridade, área, cliente, alvo de carreira, calendário e capacidade disponível. Pede avaliação anterior, matriz técnica e documentos úteis; pode começar com entradas incompletas, registrando desconhecidos. Produz diagnóstico revisável e propõe poucas prioridades. Depois cria ações, entregas, evidências previstas e cronograma.

### Jornada B — entrar no meio do ciclo

Importa o PDI existente e separa concluído, andamento, planejado, atrasado e situação desconhecida. Preserva título, descrição, prazo original, identificador externo quando disponível e links. Não retrodata uma ação criada agora. Identifica realizações ainda não registradas e evidências faltantes. Planeja apenas o tempo restante e mostra modificações propostas aos compromissos existentes.

Uma atividade marcada como finalizada com previsão futura não é automaticamente inválida: pode ter terminado antes do prazo. O sistema pergunta a data real, sem confundir previsão e execução. Ações atrasadas são mostradas e tratadas com o gestor; não são apagadas para melhorar indicadores.

### Jornada C — registrar novidade

Aceita relato, arquivo, link, feedback, transcrição, certificado ou oportunidade. Preserva a entrada original; extrai fatos e sugestões; relaciona a ações existentes. Propõe um conjunto de alterações com motivo, efeitos e esforço. O usuário revisa mudanças materiais. O estado aplicado recebe versão e histórico.

### Jornada D — preparar P2P

Reúne avanços, dificuldades, pendências e perguntas para alinhamento. Sugere pauta curta. Após a conversa, distingue decisões, sugestões e comentários. Não transforma toda frase de transcrição em compromisso.

### Jornada E — entrega parcial

Consolida o período selecionado, revisa critérios e evidências, produz ações ou atualizações para o Team Guide e ajusta o próximo período. Um marco trimestral não implica que toda ação deva começar e acabar dentro do trimestre.

### Jornada F — fechar e iniciar outro ciclo

Consolida resultados e pendências, registra a situação institucional conhecida, congela a versão de fechamento e arquiva o ciclo. Inicia novo ciclo com novas datas, regras e avaliação. Pendências só são transferidas por decisão explícita; atividades realizadas permanecem históricas e sua validade é recalculada.

## 5. Planejamento e capacidade

Cada plano deverá incluir horizonte, objetivos, prioridades, ações, dependências, esforço estimado, marcos, evidências e riscos. O cronograma combina visão geral do ciclo, consolidações trimestrais, revisão mensal e próximos passos semanais ou quinzenais.

A capacidade separa desenvolvimento dentro do trabalho e dedicação adicional voluntária. O plano deve considerar agenda do projeto, férias e períodos indisponíveis. Reservar margem para imprevistos é uma decisão de produto a ajustar com o usuário, não uma regra institucional. Proposta inicial: ocupar até 70–80% da disponibilidade declarada com ações planejadas; resto para variações.

Ordem de prioridade:

1. Critérios excludentes pendentes ou desconhecidos.
2. Compromissos já assumidos e vencimentos próximos.
3. Lacunas de desempenho, potencial e competências destacadas no feedback.
4. Ações com valor real para empresa/cliente e evidência viável.
5. Oportunidades adicionais compatíveis com capacidade e interesse.

Cada oportunidade nova deve indicar qual ação será adiada ou substituída se não houver espaço. O sistema não deve ampliar continuamente o plano. Qualquer replanejamento de ação oficial depende de alinhamento apropriado; não constitui dispensa de requisito.

## 6. Metas, OKRs e evidências

Usar poucos objetivos claros. OKRs são opcionais; critérios excludentes não viram metas aspiracionais. Exemplo fictício: objetivo de reduzir esforço de atualização do PDI; resultados-chave medem tempo antes/depois e uso recorrente, com períodos comparáveis e fonte dos dados.

Cada ação define evidências antes de começar. Diferenciar:

- Execução: material, registro ou entrega que comprova a realização.
- Qualidade: revisão, aceitação ou feedback pertinente.
- Impacto: mudança observada com medida e contexto, quando disponível.

O sistema busca comprovação suficiente e pertinente. Não recompensa volume de prints, duplicação de atividades ou afirmações ornamentadas. Uma evidência pode apoiar vários critérios se a relação for explícita; isso não multiplica o resultado ou a contagem de realizações.

Links entram no catálogo mesmo sem cópia do arquivo. Quando autorizado e disponível, guardar também o arquivo local. Um link não aberto é classificado como localização informada, não evidência inspecionada. Todas as entradas individuais acessíveis no `innie/pessoal` são armazenadas no `outtie`.

## 7. Painel e indicadores

O painel Markdown mostra: próximos passos; prazos; bloqueios; ações concluídas sem evidência; requisitos pendentes; janelas a vencer; evolução de competências; alterações aguardando revisão; pacote para próxima P2P.

| Indicador | Definição proposta |
| --- | --- |
| Cobertura de excludentes | Quantidade com comprovação confirmada / quantidade aplicável; desconhecidos aparecem separadamente |
| Cumprimento operacional do plano | Ações devidas na data de corte concluídas / ações devidas; suspensões e alterações são visíveis |
| Prontidão de evidências | Ações realizadas com pacote revisado / ações realizadas |
| Evolução de competência | Mudança documentada entre avaliações ou demonstrações, indicando quem avaliou |
| Sustentabilidade | Esforço real comparado ao disponível, atrasos e sobrecarga relatada |
| Uso e utilidade | Retorno às revisões, tempo gasto e avaliação voluntária de benefício |

Estes são indicadores do produto. Não substituem as fórmulas, notas e auditorias da empresa. Percentuais com denominador zero aparecem como não aplicáveis. Nunca mostrar probabilidade de promoção ou box previsto como resultado oficial.

## 8. Requisitos funcionais

P0: indispensável ao protótipo; P1: indispensável ao piloto; P2: posterior.

| ID | Prioridade | Requisito |
| --- | --- | --- |
| RF-01 | P0 | Capturar perfil e distinguir nível atual, nível desejado e step confirmado |
| RF-02 | P0 | Configurar datas, corte, avaliação e marcos de cada ciclo |
| RF-03 | P0 | Ingerir MD, HTML, PDF com texto, imagens e relatos, indicando limites de extração |
| RF-04 | P0 | Preservar fontes e distinguir fato, relato, inferência e decisão |
| RF-05 | P0 | Selecionar regras pela área, função, senioridade e tipo de valorização |
| RF-06 | P0 | Distinguir critérios excludentes, adicionais e não aplicáveis |
| RF-07 | P0 | Importar PDI parcial sem sobrescrever registros originais |
| RF-08 | P0 | Diagnosticar competências, feedbacks, requisitos e evidências |
| RF-09 | P0 | Criar plano com ações, esforço, dependências e cronograma |
| RF-10 | P0 | Relacionar cada ação aos objetivos e critérios pertinentes |
| RF-11 | P0 | Incorporar novidades por alterações explícitas e versionadas |
| RF-12 | P0 | Gerar título e descrição do Team Guide, com contagem de caracteres |
| RF-13 | P0 | Retomar estado em nova sessão sem depender do chat anterior |
| RF-14 | P1 | Registrar evidências, autores, datas, localização e situação de verificação |
| RF-15 | P1 | Calcular janelas de seis/doze meses na data de corte configurada |
| RF-16 | P1 | Preparar P2P e incorporar seus compromissos revisados |
| RF-17 | P1 | Consolidar marcos trimestrais e revisões mensais |
| RF-18 | P1 | Manter metas, OKRs opcionais e indicadores transparentes |
| RF-19 | P1 | Mostrar painel de pendências e capacidade |
| RF-20 | P1 | Arquivar ciclo e iniciar outro, com contexto selecionado |
| RF-21 | P1 | Conectar `outtie` anterior e migrar formatos com backup |
| RF-22 | P1 | Separar expectativas de colaborador e liderança |
| RF-23 | P1 | Exportar resumo compartilhável selecionado pelo usuário |
| RF-24 | P1 | Registrar atualização das regras e impacto nos planos |
| RF-25 | P1 | Acompanhar mudanças de cargo, cliente ou gestor com data de efeito |
| RF-26 | P1 | Registrar realização fora do trabalho sem presumir validade institucional |
| RF-27 | P2 | Oferecer catálogo de oportunidades com fonte e vigência |
| RF-28 | P2 | Suportar outras integrações mediante teste de compatibilidade |
| RF-29 | P2 | Oferecer lembretes automatizados apenas após configuração explícita |
| RF-30 | P1 | Distinguir exportação local de registro efetivo no Team Guide |

## 9. Requisitos de qualidade

| ID | Requisito e aceitação |
| --- | --- |
| RNF-01 | Dados individuais não pertencem à distribuição do `innie`; verificação Git obrigatória antes de publicar o núcleo |
| RNF-02 | Uma única interface conversacional; especialista não exige escolha manual cotidiana |
| RNF-03 | Estado estruturado persistente e documentos legíveis sem IA |
| RNF-04 | Escritas com validação, versão, recuperação e interrupção segura |
| RNF-05 | Agentes não elevam relatos a fatos comprovados nem inventam fontes |
| RNF-06 | Adapters não duplicam regras institucionais; há uma fonte canônica |
| RNF-07 | Calendário e localidade configuráveis; inicial `America/Fortaleza` |
| RNF-08 | Formatos UTF-8, datas ISO, identificadores estáveis e links relativos portáveis |
| RNF-09 | Registro mínimo de versão do VS Code, integração e modelo testado |
| RNF-10 | Arquivos fechados não são modificados pelo fluxo cotidiano |
| RNF-11 | Operações de preparação e retomada são idempotentes |
| RNF-12 | Simplicidade: sem serviços permanentes ou API própria no primeiro piloto |

## 10. Comportamentos proibidos pelo produto

Fabricar evidências; marcar tarefas como concluídas sem confirmação; excluir atrasos para inflar indicadores; inventar aprovação do gestor; assumir que todos estão no box 1C; tratar mudança de step como promoção vertical automática; usar autoavaliação como avaliação oficial; cadastrar toda sugestão como obrigação; incentivar excesso de jornada como estratégia de destaque.

Documento de arquitetura e dados: [03-arquitetura-dados-e-ciclos.md](03-arquitetura-dados-e-ciclos.md). Regras: [02-regras-institucionais-e-fontes.md](02-regras-institucionais-e-fontes.md).
