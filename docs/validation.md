# Validação e limites de evidência

## Testes locais

Executar `python3 -m unittest discover -s tests -v`. Cobrem setup/conexão, ignore/Git, revisão concorrente, falha de publicação do ponteiro, hash divergente, importação/dedupe, datas, dependências, comprovação, edição de visões, limite UTF-16, arquivo de ciclo e backup/restauração. Executar check_package para formatos, JSON e links.

Os testes foram executados no ambiente Linux de criação. Não comprovam execução de PowerShell no Windows, descoberta de agentes pelo VS Code instalado do usuário, resposta do modelo ou aprovação institucional.

## Roteiro manual no VS Code

1. Abrir em WSL2 e conferir customizações.
2. Pedir revisão atual/ciclo e comparar com state.
3. Importar fixture de PDI parcial e observar se o assistente preserva dados.
4. Revisar diagnóstico/plano e aplicar uma proposta.
5. Registrar novidade e conferir mudanças/versão.
6. Pedir P2P, marco e exportação.
7. Reiniciar a conversa e verificar retomada.
8. Fazer backup, restauração e reconectar.
9. Simular fechamento/novo ciclo com datas fictícias, sem usar ciclo real para teste destrutivo.

Conferir que o assistente não promete promoção, não confirma critério por relato isolado e não pressupõe intervalo mínimo entre promoções. Testar uma oficina curta, reconhecimento coletivo, documento misto e fonte inacessível.

## Estado do produto

Scripts implementados e testáveis; procedimentos de IA empacotados; vigência e semântica institucional pendentes de revisão apropriada; integração Copilot precisa do ensaio local. O pacote é adequado para iniciar o piloto, não uma certificação de prontidão para todos os funcionários.

## Continuidade

Registrar versão do VS Code, Copilot, modelo, cenário e resultado observado. Usar dados fictícios em testes compartilhados. Correções nas skills dependem de tarefas reais, não só de validação sintática.

## Resultado inicial da versão 0.1.0 — 2026-10-03

- 44 testes automatizados passaram em Linux/Python 3.12.
- Fluxo sintético completo conferido: configuração, importação, proposta, evidência, exportação, fechamento, novo ciclo, transferência, backup, restauração e reconexão.
- Quatorze skills passaram na validação do frontmatter; links locais e arquivos JSON conferidos.
- Compilação Python e sintaxe dos wrappers Bash verificadas.
- PowerShell/WSL2 real e inferência no Copilot permanecem para validação no computador do participante.

As fixtures são fictícias e não foram incorporadas ao outtie entregue.

## Etapa de jornada e distribuição — 2026-10-03

78 testes automatizados passaram. Novos cenários cobrem espaço ainda não preparado, status sem ciclo, rascunhos sem seleção automática, duas respostas persistidas e recuperadas, propostas pendentes/desatualizadas, calendário parcial, documentos opcionais e integridade/referências de fontes. Consultas são verificadas como somente leitura; indicadores existentes são preservados.

Check_package e validação das duas skills alteradas passaram. Uma cópia limpa do núcleo foi versionada temporariamente e clonada em duas pastas distintas; bootstrap, doctor, onboarding, status e repetição passaram, com outties distintos e árvores Git limpas. Não houve publicação, autenticação GitHub ou uso de dados individuais no ensaio.

Complemento ao roteiro manual pendente: iniciar sem documentos; responder duas perguntas; interromper; abrir outra conversa e retomar sem repetir respostas. Consultar status antes de existir plano. Conferir que `/pdi-fechar` não cria novo ciclo e `/pdi-novo-ciclo` não encerra o ativo implicitamente. Conferir caminhos/revisão nos resultados dos nove atalhos. Esses comportamentos conversacionais ainda não foram observados em um modelo no editor.
