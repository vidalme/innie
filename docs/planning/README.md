> **Planejamento histórico.** Este documento descreve a proposta original e pode mencionar etapas já implementadas. Para instalar e usar a versão atual, consulte [INSTALL](../../INSTALL.md) e o [guia do colaborador](../user-guide.md). O [CHANGELOG](../../CHANGELOG.md) registra a implementação.

# Innie / Outtie — especificação do copiloto de desenvolvimento profissional

Versão: 0.1 • Data: 03/10/2026 • Estado: planejamento para implementação e validação do piloto.

Este pacote descreve o produto, suas regras, a arquitetura, os agentes, as skills e o plano de construção. Não contém agentes instaláveis nem scripts implementados. Os caminhos, comandos e contratos apresentados são a especificação a ser implementada.

## Objetivo

Ajudar colaboradores do Atlântico a interpretar as expectativas de sua função, planejar desenvolvimento relevante, executar ações viáveis e demonstrar resultados por meio de evidências. O objetivo de valorização do piloto é preparar uma candidatura consistente a até dois steps por ciclo, respeitando as regras aplicáveis. Não existe promessa de promoção.

O sistema acompanha o trabalho entre avaliações: importa um PDI parcial, planeja o período restante, recebe novidades, prepara P2Ps e entregas trimestrais, produz ações para o Team Guide e preserva o histórico quando um novo ciclo começa.

## Como ler

| Documento | Conteúdo |
| --- | --- |
| [01-produto-e-requisitos.md](01-produto-e-requisitos.md) | Visão, escopo, jornadas, funcionalidades, métricas e catálogo de requisitos |
| [02-regras-institucionais-e-fontes.md](02-regras-institucionais-e-fontes.md) | Regras extraídas dos anexos, matriz de critérios, competências e pendências de validação |
| [03-arquitetura-dados-e-ciclos.md](03-arquitetura-dados-e-ciclos.md) | WSL2, repositórios, symlinks, dados, atualização transacional, ingresso parcial e arquivos de ciclos |
| [04-agentes-skills-e-fluxos.md](04-agentes-skills-e-fluxos.md) | Responsabilidades dos agentes, contratos das skills, entradas de conversa e revisão |
| [05-implementacao-piloto-e-validacao.md](05-implementacao-piloto-e-validacao.md) | Scripts previstos, plano de quatro semanas, cenários de aceitação, riscos e decisões |

O arquivo `Plano_Completo_Innie_Outtie.md` reúne estes documentos para leitura e compartilhamento em um único arquivo. Os documentos separados são a fonte editorial deste pacote; o consolidado é uma cópia gerada.

## Decisões confirmadas na conversa

- Piloto com André e um colega DevOps que já utiliza VS Code e Copilot.
- Ambiente inicial: Windows com WSL2 e Ubuntu; VS Code conectado à distribuição.
- Copilot é a primeira integração validada. O usuário informou que seu uso está autorizado para os dados do piloto.
- Um assistente principal visível, com responsabilidades e skills internas.
- `innie`: núcleo compartilhado internamente, sem dados individuais na distribuição.
- `outtie`: estado individual local, com Git opcional e possibilidade de reconectar um estado antigo.
- Acesso cotidiano concentrado no `innie`, por um symlink ignorado pelo Git apontando para o `outtie`.
- Datas e marcos fornecidos em cada ciclo; acompanhamento mensal e consolidações trimestrais.
- Importação de PDIs já em andamento e transição explícita entre ciclos, com arquivos rotulados pelo período.
- Saída para o Team Guide por ação: título e descrição de até 16 mil caracteres, conforme informado pelo usuário. Sem integração automática no piloto.
- Protótipo demonstrável em uma semana; versão de teste em três a quatro semanas.
- Validação com o gestor; RH acionado quando necessário para interpretar regras.

## O que a análise dos documentos acrescentou

O PDI é central para organizar desenvolvimento e comprovação, mas não é o único determinante. A política fornecida associa até dois steps ao box 1C, considera orçamento e julgamento da liderança e distingue critérios excludentes de adicionais. Há janelas de seis e doze meses e exigências específicas para comprovação. Uma autoavaliação ou uma inferência da IA não substitui a avaliação oficial de hard skills.

As datas ainda não estão fechadas. O usuário informou fechamento em maio/2027, março/2028 e março nos anos seguintes. A documentação antiga menciona julho e ressalva alterações do calendário. De 03/10/2026 a uma data em maio/2027 restam aproximadamente sete a oito meses, dependendo do dia; não nove meses. O ciclo pode ter duração total diferente do período restante. O sistema deverá calcular dias e semanas a partir das datas confirmadas, distinguindo fechamento do PDI, data de corte e avaliação.

## Limites deste pacote

Os anexos foram lidos localmente, inclusive as imagens e o relatório PDF. Referências às fontes estão no documento 02. Não foram abertos os links privados de evidências existentes no PDI. Percentuais registrados, comentários e resultados descritos nesses arquivos são tratados como informações de origem, não como auditoria externa de cada evidência.

Regras com versão 29/07/2025 precisam de confirmação de vigência para o novo ciclo. O calendário informado na conversa é uma configuração proposta, ainda sem datas diárias oficiais. Qualquer recomendação além das regras documentadas aparece como decisão de produto ou hipótese de planejamento.

## Resultado esperado do piloto

Um colega consegue preparar seu ambiente, importar contexto, revisar um diagnóstico, adotar um plano executável, registrar uma novidade e produzir uma ação verificável para o PDI com pouca intervenção do criador. O histórico sobrevive a atualizações do `innie` e à troca de ciclo.
