# Innie — Copiloto de Desenvolvimento

**Versão 0.1.0: implementação inicial para piloto em VS Code + Copilot + Ubuntu/WSL2.**

O produto ajuda colaboradores a transformar regras de avaliação, feedbacks e objetivos de carreira em um plano executável, acompanhado por evidências. O objetivo do piloto é melhorar preparação para valorização, inclusive até dois steps quando elegível. O sistema não concede promoção nem prevê a decisão da liderança.

## Por que existe

Regras e informações ficam espalhadas em documentos, avaliações, P2Ps, entregas e evidências. O fechamento do ciclo vira trabalho de reconstrução. O copiloto organiza decisões e comprovação durante o ciclo, aceita entrada no meio do período e preserva o histórico quando outro ciclo começa.

## Quem usa e quem mantém

- Colaborador: usa o assistente, executa ações e revisa os registros.
- Gestor: alinha prioridades e interpreta as expectativas.
- Mantenedor: atualiza o núcleo, as fontes e a integração.
- RH/P&C: confirma regras, vigência e exceções quando necessário.

Primeiro piloto: dois profissionais DevOps. Estrutura preparada para outras trilhas, que exigirão suas matrizes e revisão. Dados individuais não são compartilhados automaticamente com a liderança.

## Começar

Extrair o pacote mantendo `innie` e `outtie` como pastas irmãs dentro do filesystem Linux do WSL. No terminal Ubuntu:

```bash
cd ~/pdi-copilot/innie
bash scripts/bootstrap.sh
python3 scripts/pdi.py doctor
code .local/pdi.code-workspace
```

Selecionar o agente **copiloto-desenvolvimento** no chat e escrever “Quero começar; já tenho um PDI parcialmente preenchido”. Se preferir, usar `/pdi-iniciar`. O ambiente precisa de autenticação/licença Copilot e descoberta das customizações; faça o teste descrito em [INSTALL.md](INSTALL.md).

O bootstrap verifica Python e Git e termina com uma orientação legível: destino individual, workspace a abrir, revisão/ciclo a conferir no assistente e primeiro atalho. A preparação local e a verificação do assistente no editor são etapas distintas. Para automação, `bash scripts/bootstrap.sh setup --format json` devolve os mesmos dados e próximos passos em JSON.

O `outtie` distribuído é vazio de informações pessoais. O link `pessoal` é criado pelo setup e ignorado pelo Git. Cada pessoa conecta seu próprio espaço, que pode ser uma pasta local ou um repositório privado opcional.

## O que já funciona nos scripts

Preparação, conexão de espaço existente, Git local opcional, importação de arquivos, propostas revisadas, revisões verificadas, validação, calendário por ciclo, indicadores operacionais, janela de meses, visões Markdown, exportação com limite, backup/restauração, arquivo de ciclo, transferência de ação pendente e adendo. Os testes não dependem de um modelo ou serviço externo.

## O que é feito pelo Copilot

Interpretação de documentos, diagnóstico, planejamento, associação qualitativa de evidências, preparação de P2P, síntese de marcos e redação. Sete agentes e catorze skills fornecem os procedimentos. A interpretação é revisável e não substitui avaliação oficial.

## Limites explícitos

Não há escrita automática no Team Guide, envio de mensagens, RAG/MCP, previsão de promoção ou servidor permanente. Não foram executados testes de inferência dentro do VS Code do participante. O acesso do Copilot a symlinks/arquivos ignorados e a descoberta de agentes devem ser validados localmente; o setup já gera um workspace com duas raízes.

Regras de 2025 estão processadas e marcadas para confirmação de vigência. Datas exatas do ciclo não são pré-preenchidas. Não foi confirmada uma regra de intervalo mínimo entre promoções. `migrate` reconhece o schema 1; schemas desconhecidos são preservados e exigem migração assistida futura.

## Documentação

| Documento | Conteúdo |
| --- | --- |
| [INSTALL.md](INSTALL.md) | Preparação, WSL, conexão e primeiro uso |
| [docs/user-guide.md](docs/user-guide.md) | Fluxos de uso cotidiano |
| [docs/architecture.md](docs/architecture.md) | Componentes, memória, symlink e decisões de implementação |
| [docs/data-contracts.md](docs/data-contracts.md) | Estado e entidades |
| [docs/proposals.md](docs/proposals.md) | Operações revisáveis e exemplos |
| [docs/scripts.md](docs/scripts.md) | Referência completa da CLI e scripts auxiliares |
| [docs/agents-and-skills.md](docs/agents-and-skills.md) | Responsabilidades e como manter customizações |
| [docs/cycles.md](docs/cycles.md) | Ingresso parcial, fechamento, recuperação e ciclo novo |
| [docs/maintenance.md](docs/maintenance.md) | Publicação dos repos, fontes, testes e atualizações |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Falhas e procedimentos de recuperação |
| [docs/validation.md](docs/validation.md) | Evidências dos testes e roteiro de teste no VS Code |
| [docs/planning/README.md](docs/planning/README.md) | Especificação original completa; referência histórica de escopo |

## Publicar e contribuir

Publicar o `innie` no repositório interno da empresa; seu conteúdo institucional não é destinado a publicação aberta. Nunca publicar o `outtie` no origin do `innie`. A inicialização Git não configura remotes nem faz push. Consulte [manutenção](docs/maintenance.md) para separar os repositórios.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```

Arquitetura e comportamento implementados prevalecem sobre detalhes de caminho do plano histórico. Confira o CHANGELOG para decisões e limitações da versão.
