# Diagnóstico e recuperação

| Sintoma | Procedimento |
| --- | --- |
| Python ausente/antigo ou Git ausente | Instalar Python 3.11+ e Git no Ubuntu/Linux; no Ubuntu, `bash scripts/install.sh --install-deps` oferece a instalação explícita. No Windows, executar os scripts dentro do Ubuntu/WSL2 |
| Doctor retorna not_initialized | Executar `bash scripts/bootstrap.sh` e seguir a orientação de primeiro uso; o diagnóstico não cria o espaço |
| Copilot não vê agentes | Conferir janela WSL, versão/extensão, workspace e painel de customizações; não depender só do nome da pasta |
| Estado não carregado pelo modelo | Pedir leitura explícita de metadata/revisão; abrir `.local/pdi.code-workspace`, gerado com duas raízes por padrão |
| Symlink quebrado | Conferir destino real, conectar outtie correto com script; não criar cópia concorrente |
| pessoal é pasta real | Preservar e fazer backup; não removê-la para instalar link |
| Outro outtie conectado | Revisar destinos e usar connect --switch; ambos permanecem |
| Espaço individual existente sem vínculo | Conferir o caminho mostrado; usar `--outtie CAMINHO connect` para escolhê-lo ou `--outtie NOVO_CAMINHO setup` para criar outro |
| Schema desconhecido | Preservar originais; criar novo espaço e importar; migrate não converte arbitrariamente |
| Proposta desatualizada | Ler state novamente e recriar proposta, preservando motivo; não editar expected_revision |
| Hash divergente | Parar edições, preservar pasta e restaurar backup em destino novo |
| Edição manual em outputs | Usar preserve-edits para guardar cópia na inbox; revisar conteúdo como proposta |
| Arquivo de evidência ausente | Restaurar material/importar corretamente; não marcar evidência inspecionada |
| PDF sem texto ou pdftotext ausente | Instalar ferramenta opcional ou fornecer texto/inspeção manual; original preservado |
| Falha de close após criar archive | Reexecutar com mesma revisão; divergência exige inspeção, não sobrescrita |
| Lock ocupado | Esperar operação ativa terminar; não remover lock para forçar concorrência |
| Git rastreia pessoal | Não publicar; corrigir índice/histórico conforme política interna |
| Backup excede 512 MiB na restauração | Preservar arquivo e planejar restauração assistida/revisar limite no código com testes |

O doctor verifica filesystem e estado, não a autenticação/qualidade do modelo. Sem acesso a ferramentas, o assistente deve produzir uma proposta e orientar sua aplicação, não afirmar que executou.

## Recuperar sem adulterar dados

Fazer cópia da instalação afetada; restaurar backup em pasta nova; executar validate e connect no novo destino; verificar painel. Snapshots e recibos podem ajudar um mantenedor a investigar uma falha, mas o usuário não deve editar metadata para esconder divergências.

Backup preserva a proveniência das visões em `.runtime/views.json`, mas exclui locks e arquivos temporários. Visões intactas podem ser regeneradas após restaurar; alterações manuais continuam exigindo `render --preserve-edits`. As revisões canônicas continuam verificadas.
