# 02 — Regras institucionais, fontes e validação

## 1. Status e método

Esta é uma interpretação inicial dos documentos enviados para orientar implementação e revisão com o gestor. A versão das três matrizes HTML é 29/07/2025. Nenhuma regra é declarada vigente para 2027 apenas porque foi anexada: sua aplicação ao ciclo será confirmada e registrada.

Preservar texto de origem, regra extraída, referência de seção/linha/página, escopo, versão e decisão de revisão. Quando duas fontes divergem, registrar ambas e a pendência. Uma conversa recente pode atualizar uma configuração pessoal, mas não revoga por si só uma norma institucional.

## 2. Inventário dos 15 anexos

| ID | Arquivo de origem | Natureza e uso |
| --- | --- | --- |
| I01 | `Avaliação de Desempenho(1).md` | Institucional: processo, escala, hard skills e normalização |
| I02 | `PDI - Plano de Desempenho Individual(1).md` | Institucional: ações, competências, acompanhamento mensal e 70:20:10 |
| I03 | `Formulário Avaliação de Desempenho(2).md` | Institucional: perguntas e expectativas por senioridade |
| I04 | `promoção-e-bonificação(2).md` | Institucional: tipos de valorização, 9box, orçamento e elegibilidade |
| I05 | `Critérios Institucionais(2).html` | Institucional: excludentes e adicionais; versão 29/07/2025 |
| I06 | `Critérios adicionais Operação(2).html` | Institucional: critérios da Operação; versão 29/07/2025 |
| I07 | `DevOps(2).html` | Misto: matriz institucional de competências e comentários pessoais/IA; separar antes de distribuir |
| I08 | `9box.png` | Ilustração institucional: posição dos boxes e eixos |
| P01 | `metas.md` | Exportação individual: instruções detalhadas de evidência misturadas a percentuais e datas pessoais |
| P02 | `ultimo_pdi_preenchido.md` | Individual: ações, previsões, estados e links; teste de importação |
| P03 | `ResultadoAvaliação(2).pdf` | Individual: relatório de 16 páginas, classificação, comentários e autoavaliação |
| X01 | `sample_resultado.png` | Exemplo ilustrativo de relatório; não usar como escala atual do colaborador |
| X02 | `tabela_salarial.md` | Referência de steps e faixas por família; não contém valores monetários de salários |
| X03 | `tabela_salarial_01.png` | Recorte visual de famílias de cargos e steps |
| X04 | `tabela_salarial_02.png` | Recorte complementar; não tratar isoladamente como tabela completa |

Somente a matriz limpa de I07 pertence ao `innie`. As anotações pessoais permanecem no `outtie`. Em P01, instruções potencialmente institucionais podem ser extraídas para revisão, mas percentuais e estados pessoais não devem ser distribuídos. P02 e P03 não compõem a base compartilhada. Os links de evidências contidos nesses arquivos não foram acessados nesta análise.

## 3. Política de valorização e objetivo de dois steps

Fonte: I04, seções “Tipos de Valorização”, “O que é considerado na análise?”, “Matriz 9Box” e “Regras de Valorização”; I08 para orientação visual.

| Tipo | Definição na fonte |
| --- | --- |
| Progressão horizontal | Aumento salarial sem alteração de função/senioridade |
| Promoção vertical | Mudança de função e/ou senioridade, com ampliação de escopo |
| Bonificação | Reconhecimento financeiro pontual |

| Box | Possibilidades previstas na política fornecida |
| --- | --- |
| 1C | Horizontal até dois steps, vertical e/ou bonificação até 60% do salário |
| 1B ou 2C | Horizontal um step e/ou bonificação até 40% |
| 2B | Bonificação até 20% |

Estas possibilidades não são automáticas. A análise inclui avaliação de desempenho, matriz 9box, critérios institucionais, orçamento e contexto considerado pela liderança. A política não estabelece, no material fornecido, um número de critérios adicionais que garanta dois steps.

Desempenho resulta dos blocos de soft skills e resultados; potencial, do bloco de potencial. A metodologia exata de agregação/pesos e os limites do ciclo precisam ser obtidos para qualquer cálculo institucional. I01 descreve uma normalização estatística, mas não fornece o algoritmo. I04 informa acesso da liderança à matriz. O sistema não deve inferir um box oficial pela classificação geral “Destaque”.

I08 mostra 1C como desempenho e potencial acima do esperado. A linha 1 corresponde a desempenho acima, linha 2 dentro, linha 3 em desenvolvimento; coluna A corresponde a potencial em desenvolvimento, B dentro, C acima. Representar os eixos corretamente evita inverter a interpretação.

Se dois steps atravessarem uma faixa de senioridade, distinguir as regras horizontais e verticais. O sistema não deve concluir que o avanço é automático nem que os dois aumentos terão necessariamente a mesma forma de concessão. X02 serve para formular a pergunta à gestão, não para determinar o enquadramento DevOps sem confirmação da família aplicável.

## 4. Critérios institucionais

Fonte: I05, linhas 9–17 da planilha exportada. Excludente significa que o não atendimento inabilita para o tipo em questão; adicional favorece análise, mas não é obrigatório para elegibilidade.

| ID | Critério | Horizontal | Vertical | Bonificação |
| --- | --- | --- | --- | --- |
| CI-01 | 100% das hard skills da função/senioridade atual, exceto inglês | Não se aplica | Excludente | Adicional |
| CI-02 | Pelo menos 70% das hard skills atuais, exceto inglês | Excludente | Não se aplica | Não se aplica |
| CI-03 | Pelo menos 70% das hard skills da função/senioridade desejada, exceto inglês | Não se aplica | Excludente | Não se aplica |
| CI-04 | 100% dos treinamentos obrigatórios institucionais definidos para o ano | Excludente | Excludente | Excludente |
| CI-05 | 100% das ações previstas no PDI até o período de análise | Excludente | Excludente | Excludente |
| CI-06 | Participação ativa em iniciativa interna | Adicional | Adicional | Adicional |
| CI-07 | Treinamento interno de um turno para disseminar conhecimento nos últimos seis meses | Adicional | Adicional | Adicional |
| CI-08 | Ação de promoção da marca no ecossistema cearense | Adicional | Adicional | Adicional |
| CI-09 | Melhoria/inovação com impacto mensurável em eficiência, qualidade ou resultados estratégicos | Adicional | Adicional | Adicional |

O produto deve priorizar CI-04 e CI-05, mas não orientar um plano artificialmente vazio para obter 100%. Planejar compromissos realistas e manter histórico de mudanças. Se algo precisar ser cancelado ou replanejado, alinhar e registrar a decisão; não presumir que a alteração mantém elegibilidade.

## 5. Critérios adicionais da Operação

Fonte: I06, linhas 9–16. Todos são adicionais para progressão, promoção vertical e bonificação.

| ID | Critério | Janela explícita |
| --- | --- | --- |
| OP-01 | Inglês no nível esperado para função/senioridade | Não especificada nesta matriz |
| OP-02 | Reconhecimento formal do cliente | Últimos 12 meses |
| OP-03 | Submissão de artigo científico ou depósito de propriedade intelectual em interesse institucional | Últimos 12 meses |
| OP-04 | Participação em PoC da IN&N | Últimos 12 meses |
| OP-05 | Uma certificação alinhada às necessidades organizacionais | Últimos 12 meses |
| OP-06 | Contribuição transversal entre projetos/portfólios | Últimos 12 meses |
| OP-07 | Ampliação do nível de formação | Últimos 12 meses |
| OP-08 | Adaptação a função, mercado, metodologia ou tecnologia | Últimos 12 meses |

Não tratar todos os adicionais como metas obrigatórias simultâneas. Escolher ações relevantes e viáveis; não recomendar uma graduação concluída em poucos meses a quem ainda não está nessa condição.

## 6. Qualificação das evidências

Fonte complementar: P01, texto descritivo de cada meta. Estas instruções precisam ser confirmadas para o novo ciclo; suas datas pessoais e percentuais não são regras gerais.

| Critério | Especificidade extraída de P01 |
| --- | --- |
| Hard skills | Avaliação da liderança imediata e imagem da comparação; autoavaliação não substitui |
| Inglês | Certificado Geo English; condições de aplicação do teste descritas na fonte |
| Formação | Certificado/declaração de conclusão do nível de escolaridade; disciplinas isoladas não bastam |
| Marca | Material de representação/publicação/participação; curtidas, comentários e compartilhamentos não bastam |
| Transversalidade | Confirmação por e-mail do GP ou gerente executivo, conforme função |
| Inovação | Antes/depois, materiais, ações, validação do gestor ou prova equivalente; impacto mensurável |
| Iniciativa interna | Participação voluntária fora da atividade-fim/obrigação; contribuição efetiva comprovada |
| PoC IN&N | Confirmação do coordenador de P&D ou líder de plataforma |
| PDI | Print mostrando ações devidas concluídas e ausência de atraso |
| Obrigatórios | Tela de conclusão de trilhas/certificados; lista e prazo devem ser os do novo ciclo |
| Treinamento ministrado | Voluntário, fora das obrigações; lista, avaliação de reação, apresentação ou equivalente; duração exigida deve ser demonstrada |
| Reconhecimento do cliente | Formal, datado e dirigido à pessoa; reconhecimento coletivo não basta |
| Adaptação | Confirmação do GP/gerente executivo e contribuição demonstrada |
| Artigo/IP | Comprovação da submissão ou depósito; texto informal não equivale a artigo científico |
| Certificação | Certificado datado e alinhamento às necessidades organizacionais |

Uma palestra curta não se torna automaticamente um treinamento de um turno. Um projeto interno pode apoiar inovação, colaboração e participação, mas cada relação precisa de comprovação própria. Não afirmar que este copiloto é uma PoC IN&N apenas por ser uma prova de conceito técnica.

## 7. Competências e expectativas

I03 distingue seis competências comportamentais comuns: pensamento crítico, comunicação sem inglês, colaboração, pensamento criativo, inteligência social e inteligência emocional. Resultados: alcance de metas, qualidade do trabalho e produtividade. Potencial: desenvolvimento profissional, adaptação e potencial de crescimento. Há três perguntas específicas para liderança: influência/engajamento, delegação e formação de novas lideranças. Só ativá-las quando o perfil estiver no escopo de liderança.

As expectativas variam por senioridade e devem ser consultadas pelo sistema para o nível atual e o desejado. Demonstrar tarefas complexas não comprova automaticamente todos os aspectos de um nível superior. Autonomia, impacto coletivo e consistência precisam ser observados de maneira contextualizada.

I01 apresenta os níveis técnicos: sem conhecimento; conhecimento teórico; CH básico; CH intermediário; CH avançado; multiplicador. Inglês utiliza escala própria. Uma codificação ordinal interna pode apoiar comparações, mas somar esses códigos para calcular o percentual oficial não é autorizado pela documentação.

### Matriz DevOps relevante ao primeiro piloto

Extraída de I07, colunas Júnior e Pleno. As anotações pessoais foram excluídas desta tabela.

| Competência | Júnior | Pleno |
| --- | --- | --- |
| Inglês | Nível 2 | Nível 2+ |
| Metodologias Ágeis | CH básico | CH intermediário |
| Administração de BD | Conhecimento | CH intermediário |
| Computação em Nuvem | CH básico | CH intermediário |
| Administração de Servidores | CH básico | CH intermediário |
| Containers | CH básico | CH intermediário |
| Segurança de Aplicação | Conhecimento | CH básico |
| Automação, Ansible ou similares | CH básico | CH intermediário |
| IaC, Terraform ou similares | CH básico | CH intermediário |
| Linguagem de Programação | CH básico | CH intermediário |
| Linguagem de Script | CH básico | CH intermediário |
| Pipelines CI/CD | CH básico | CH intermediário |
| Versionamento | CH básico | CH intermediário |
| Orquestração, Kubernetes ou similares | CH básico | CH intermediário |

São 13 competências não relacionadas a inglês nesta exportação. A forma oficial de avaliar atendimento parcial e calcular 70%/100% não foi encontrada. Até confirmação, importar o resultado institucional com origem identificada e apresentar lacunas descritivas. Se houver uma métrica experimental por contagem, rotulá-la como estimativa do produto e mantê-la separada da elegibilidade oficial.

I02 recomenda vincular ações a competências, planejar até um ano, utilizar avaliação como insumo e acompanhar mensalmente em P2Ps. O modelo 70:20:10 orienta combinar prática, interação e formação; não é uma quota documental nem uma exigência de horas a impor ao usuário.

## 8. Observações que orientam testes

- P02 mistura ações de períodos distintos e prevê datas futuras em itens finalizados. Preservar e pedir data real; não assumir que todos pertencem ao mesmo ciclo.
- P02/P03 apresentam relatos de produtividade com baselines diferentes. Registrar período e população medidos; não consolidar esses números em uma única melhoria nem repetir porcentagens sem recalcular.
- P03 mistura comentários e autoavaliação. Manter categoria de autoria somente quando a fonte a identificar; comentários anônimos não devem ser atribuídos ao gestor por conjectura.
- Uma autoavaliação alta não estabelece posição oficial 9box. Notas agregadas, individuais e normalizadas são campos distintos.
- X01 usa uma escala ilustrativa diferente da escala do relatório pessoal. Exemplos visuais não definem limites de ciclos futuros.
- O material de steps é incompleto para inferir a família específica de DevOps e não apresenta salários monetários. Usar o step informado/confirmado e perguntar sobre transições de faixa.

## 9. Pendências institucionais

| ID | Pergunta | Efeito no produto |
| --- | --- | --- |
| PV-01 | As regras de 29/07/2025 continuam vigentes? | Versão ativa do pacote institucional |
| PV-02 | Quais são início, cortes parciais, fechamento do PDI e avaliação? | Cálculo do cronograma e validade |
| PV-03 | Como se calcula o percentual de hard skills? | Elegibilidade técnica oficial |
| PV-04 | Quais são os limites/pesos e tratamento de notas do novo ciclo? | Exibir resultados sem simulação indevida |
| PV-05 | Como tratar travessia de faixa de senioridade e até dois steps? | Distinguir horizontal/vertical |
| PV-06 | Quais treinamentos são obrigatórios neste ano/ciclo? | Checklist de excludentes atualizado |
| PV-07 | Como interpretar meses, limites inclusivos e data de referência das janelas? | Validade e casos no limite |
| PV-08 | Existem sobreposições/exceções por cliente, vertical e função? | Seleção de critérios |
| PV-09 | Como alterar/cancelar ações oficiais sem descumprir CI-05? | Replanejamento rastreável |
| PV-10 | Qual limite real e formato dos campos do Team Guide? | Validar 16 mil caracteres e exportação |
| PV-11 | A descrição das evidências em P01 vale para o próximo ciclo? | Critérios de revisão |
| PV-12 | Bonificação máxima/política atual coincide com I04? | Evitar propagar percentuais desatualizados |

Estas pendências não impedem construir o protótipo. Impedem declarar elegibilidade ou resultados oficiais que dependam delas.

## 10. Referências técnicas verificadas em 03/10/2026

- [Custom agents no VS Code](https://code.visualstudio.com/docs/agent-customization/custom-agents): arquivos de agentes e configuração por harness.
- [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills): procedimentos e recursos carregados quando relevantes.
- [Prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files): atalhos para fluxos de conversa.
- [VS Code com WSL](https://code.visualstudio.com/docs/remote/wsl): execução conectada à distribuição.
- [Arquivos no WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems): escolha de localização compatível com ferramentas Linux.
- [Git ignore](https://git-scm.com/docs/gitignore): arquivos rastreados não são afetados; padrões de diretório não correspondem a symlinks.

Essas referências apoiam a integração, não tornam o desenho proposto uma implementação pronta. Descoberta de customizações, ferramentas disponíveis e leitura de caminhos ignorados serão verificadas na versão instalada do piloto.
