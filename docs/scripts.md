# Scripts e CLI — referência

Executar no Ubuntu/WSL2 com Python 3.11+. Entrada: `python3 scripts/pdi.py`. `--outtie PATH` é uma opção global e deve vir **antes** do comando. Sem ela, resolve symlink pessoal ou configuração local. Sem vínculo, a pasta irmã outtie é sugerida para criação; se já contiver estado, o comando orienta uma conexão explícita antes de usá-lo. Isso também impede que `state` ou `doctor` assumam automaticamente um espaço vizinho.

## Preparação

| Comando | Efeito |
| --- | --- |
| `setup [--no-two-roots] [--format json/text]` | Verifica Python/Git, inicializa formato vazio ou valida o espaço já conectado e orienta primeiro uso; estado existente sem vínculo exige connect explícito |
| `connect [--switch] [--no-two-roots] [--format json/text]` | Verifica Python/Git, conecta estado existente e orienta conferência; troca exige flag, não apaga o anterior |
| `doctor` | Verifica schema/hash, filesystem, link, Git e ferramentas opcionais; teste Copilot é manual |
| `init-git [--scope outtie ou innie]` | git init local, idempotente, sem stage/commit/remote/push |
| `migrate` | Reconhece schema atual; recusa/desconhece outros formatos sem modificá-los |

Duas raízes são o padrão; `--two-roots` continua aceito. `--no-two-roots` gera somente a raiz innie no workspace local. Exemplo: `python3 scripts/pdi.py --outtie ../outtie connect`. `setup` não converte uma pasta arbitrária preenchida sem metadata; preservá-la e usar importação assistida. Versão atual só tem schema 1, então não há migração histórica implementada.

Para usar um estado existente pela primeira vez, conferir o destino exibido e executar `python3 scripts/pdi.py --outtie CAMINHO connect`. `--outtie CAMINHO setup` também exige essa conexão prévia quando há estado no destino. Instalações já vinculadas pelo symlink ou pela configuração local continuam aceitando setup repetido. Para inspecionar um espaço sem conectá-lo, usar `python3 scripts/pdi.py --outtie CAMINHO state` explicitamente.

Setup/connect da CLI mantêm JSON por padrão, incluindo `local_ready`, ambiente, `context_to_verify`, `copilot_context: manual_check_required` e `next_steps`. `--format text` apresenta essa orientação diretamente. O bootstrap sem argumentos e o instalador usam texto; com `bash scripts/bootstrap.sh setup --format json`, automações recebem JSON. Nenhum desses comandos abre o editor ou valida autenticação do Copilot automaticamente.

Antes de setup, `doctor` devolve `state: not_initialized`, `setup_required: true` e orientação, sem criar arquivos (saída 1). Estado corrompido devolve `state: error` e orienta recuperação, sem encaminhar nova inicialização. Ambiente local válido mantém `ok: true`; o campo `copilot_context` continua indicando a verificação manual necessária.

## Fontes, estado e alterações

| Comando | Efeito |
| --- | --- |
| `import ARQUIVO [--kind personal/mixed/institutional/example] [--title TEXTO]` | Copia original, hash/dedupe, extração quando possível |
| `state` | Exibe snapshot completo atual |
| `onboarding [--cycle ID] [--format json/text]` | Orienta início/retomada, lista lacunas, notas e propostas pendentes; somente leitura |
| `validate` | Valida estrutura, status, datas, referências e hash |
| `criteria [--type horizontal/vertical/bonus] [--cycle ID]` | Lista critérios aplicáveis à área após conferir a versão do ciclo com o catálogo; vigência/elegibilidade continuam pendentes |
| `proposal --changes JSON --reason TEXTO` | Valida operações e guarda proposta na revisão corrente |
| `apply --proposal CAMINHO --approve` | Aplica sob lock após revisar; conflitos interrompem |
| `render [--cycle ID] [--preserve-edits]` | Regenera plano/painel do ciclo aberto; preserva edição divergente quando solicitado |
| `status [--cycle ID] [--on AAAA-MM-DD] [--format json/text]` | Indicadores e orientação; sem ciclo ativo, apresenta rascunhos/próximos passos; somente leitura |
| `export ACTION_ID [--cycle ID] [--max-chars 16000] [--preserve-edits]` | MD/JSON para copiar ao Team Guide; conta caracteres e unidades UTF-16 |

Texto não é resumido automaticamente pelo export: se exceder limite, revisar no assistente. Imagens/PDF sem texto não são interpretados pelo import. pdftotext é opcional; resultado visual exige conferência. Arquivos binários são preservados.

Em `status`, esforço ausente/null deixa o total pendente e aparece em `actions_missing_effort`; `known_remaining_effort_hours` mantém a soma parcial. Uma sobrecarga já demonstrada por essa soma retorna true; estimativas incompletas não retornam false. Se faltar fuso no perfil, a data automática usa America/Fortaleza e sinaliza `reference_timezone_assumed: true`. Com `--on`, a data é explícita e `reference_timezone` fica null. Em `criteria`, `area_pending: true` indica que só foram selecionados critérios comuns e ainda falta confirmar a área.

O `status` expõe `onboarding.policy_alignment` para o ciclo consultado. `criteria`, ativação e fechamento recusam versões divergentes entre ciclo, índice institucional e catálogo. Revise as regras e atualize a versão do ciclo por proposta antes de prosseguir. Isso não confirma vigência institucional nem altera archives anteriores.

## Ciclos

```bash
python3 scripts/pdi.py cycle create ciclo-id --label "Rótulo" --start AAAA-MM-DD --end AAAA-MM-DD --cutoff AAAA-MM-DD --evaluation AAAA-MM-DD
python3 scripts/pdi.py cycle start ciclo-id --reviewed
python3 scripts/pdi.py cycle close ciclo-id --approve
python3 scripts/pdi.py cycle verify pessoal/archives/NOME_RETORNADO
python3 scripts/pdi.py cycle carry --from antigo --to novo --action action-id --due AAAA-MM-DD --approve
python3 scripts/pdi.py cycle adendum antigo --file ARQUIVO --reason "Resultado oficial recebido" --approve
```

Create aceita omitir datas para um rascunho. Start exige início/fim/corte, revisão e ausência de outro ativo. Close exige ciclo ativo. Carry exige origem arquivada e destino aberto, não transfere ações done e remove evidências/resultados da nova ação. Mantém referência à origem e pendência antiga. Adendum preserva snapshot do archive e cataloga o documento tardio fora dele.

## Datas e backup

```bash
python3 scripts/pdi.py window --event AAAA-MM-DD --cutoff AAAA-MM-DD --months 12
python3 scripts/pdi.py backup --destination /OUTRO_LOCAL/backup.zip
python3 scripts/pdi.py restore /OUTRO_LOCAL/backup.zip --destination /NOVO_LOCAL/outtie-restaurado
```

Window usa meses de calendário; datas exatamente no limite recebem boundary_pending sem `--boundary-confirmed`. Essa flag só deve ser usada após confirmar a convenção institucional. Backup deve ser arquivo novo fora do outtie e exclui Git, locks, cache e backups internos. Restore exige pasta inexistente e aceita até 512 MiB descompactados, verifica paths, hashes e estado.

## Scripts auxiliares

- `bootstrap.sh`: sem argumentos executa setup; com argumentos encaminha à CLI. Não instala dependências.
- `install.sh`: setup; instala Python/Git/Poppler com apt apenas com `--install-deps`.
- `windows-prepare.ps1`: preparação opcional de WSL/VS Code com flags explícitas; exige ambiente Windows.
- `acquire.py`: clona núcleo via URL HTTPS/SSH fornecida, sem credenciais embutidas.
- `check_package.py`: verifica estrutura das customizações, JSON, links, proveniência e separação da distribuição; sem instalar skills pessoais.

## Saídas e erros

JSON em stdout por padrão; setup, connect, onboarding e status aceitam `--format text`. Erro legível em stderr. Exit 0: sucesso; 1: doctor identificou falha; 2: operação recusada/entrada inválida. Não interpretar um erro como aplicação parcial bem-sucedida. Em conflito, ler state novamente. Em hash divergente, parar e restaurar; não recalcular hash para mascarar uma edição manual.

Scripts não têm dry-run geral: proposal é o estágio candidato de estado, e comandos mutáveis de ciclo possuem revisão explícita. Fontes são importadas diretamente porque preservam entradas autorizadas. Operações remotas de publicação são manuais.
