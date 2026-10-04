# Instalação e primeiro uso — Windows / Ubuntu WSL2

## Pré-requisitos

Windows com WSL2 Ubuntu, VS Code, extensão WSL e Copilot autorizado. Python 3.11 ou superior e Git dentro do Ubuntu. A CLI utiliza somente a biblioteca padrão; não precisa de pip, API key ou venv. Poppler é opcional para extrair texto de PDF.

Verificar a distribuição no PowerShell: `wsl --list --verbose`. Se a distribuição não existir ou não estiver em versão 2, seguir [documentação oficial WSL](https://learn.microsoft.com/windows/wsl/install). O script opcional `scripts/windows-prepare.ps1` oferece `-InstallWSL` e `-InstallVSCode`; pode exigir privilégios e reinício. Ele não instala credenciais Copilot nem configura contas.

## 1. Clonar o núcleo

Obter com o mantenedor o endereço do repositório interno e acesso pelo Git corporativo. No terminal Ubuntu, substituir o endereço abaixo:

```bash
git clone URL_DO_REPOSITORIO_INTERNO ~/pdi-copilot/innie
```

Cada participante usa seu próprio clone e espaço individual. O bootstrap cria o `outtie` fora do núcleo; não é necessário clonar ou receber dados de outra pessoa. Para aquisição automatizada, `scripts/acquire.py --innie-url URL --destination CAMINHO` apenas clona e usa a autenticação do Git.

Como alternativa sem Git remoto, extrair somente o núcleo de um ZIP autorizado para uma pasta `innie` no filesystem Linux. Não copiar `.git`, `.local`, `pessoal` ou um outtie de outra pessoa. A preparação a seguir é a mesma; Git local continua sendo pré-requisito.

## 2. Preparar

No Ubuntu:

```bash
cd ~/pdi-copilot/innie
python3 --version
bash scripts/bootstrap.sh
python3 scripts/pdi.py doctor
code .local/pdi.code-workspace
```

Se Python/Git/Poppler estiverem ausentes, o instalador opcional executa apt somente com a flag explícita:

```bash
bash scripts/install.sh --install-deps
```

Sem essa flag, `bash scripts/install.sh` prepara o espaço e mostra os próximos passos. `bash scripts/bootstrap.sh` sem argumentos também executa setup com saída legível; com argumentos, encaminha o comando à CLI. Para escolher outro destino: `bash scripts/install.sh --outtie ../meu-outtie`. Instalação não publica arquivos.

Preparação exige Python 3.11+ e Git e confere esses pré-requisitos antes de criar o espaço. O comando `code` é opcional: se não estiver no terminal, a mensagem orienta abrir o workspace pela interface do VS Code. Poppler também é opcional; sua ausência permite começar com outros textos ou leitura manual de PDF. O bootstrap mostra a revisão/ciclo que deve coincidir com a leitura do assistente, cujo acesso ainda precisa ser conferido no editor.

Para saída estruturada: `bash scripts/bootstrap.sh setup --format json`. A CLI direta mantém JSON por padrão; use `python3 scripts/pdi.py setup --format text` ou `python3 scripts/pdi.py --outtie CAMINHO connect --format text` para orientação legível.

Se o destino já contiver um estado individual e esta instalação ainda não estiver conectada a ele, a preparação para e mostra seu caminho. Confira se é o espaço que deseja usar e faça a conexão explícita conforme a seção abaixo. Para começar com outro espaço, escolha um destino novo com `python3 scripts/pdi.py --outtie ../meu-novo-outtie setup`. Mantenha uma pasta de instalação própria por pessoa. Após conectar, repetir o bootstrap reutiliza o vínculo existente.

## 3. Conferir o Copilot

Confirmar que a janela do VS Code mostra conexão ao Ubuntu/WSL e a conta Copilot está autenticada. Abrir as customizações de chat e verificar agente `copiloto-desenvolvimento`, catorze skills e prompts `pdi-*`. O local da interface pode variar conforme versão.

Selecionar o assistente e pedir: “Leia minha revisão atual, informe ciclo ativo e não modifique nada”. A resposta deve coincidir com `python3 scripts/pdi.py state`. Se não conseguir ler, seguir troubleshooting, usando caminhos explícitos e conferindo as duas raízes do workspace local. O doctor testa filesystem, não o contexto do modelo.

## 4. Primeiro plano

Usar `/pdi-iniciar`. O assistente verifica ciclos e respostas já registrados, pergunta se existe PDI e solicita somente o necessário para o próximo resultado. Cargo, objetivo, disponibilidade e datas podem ser preenchidos aos poucos; datas desconhecidas ficam pendentes em um rascunho.

Documentos são opcionais para começar. Se houver avaliação anterior ou PDI parcial, usar `/pdi-importar`; eles entram no `outtie`, nunca em knowledge. Revisar a proposta antes de aplicar compromissos. Para retomar outra sessão, usar `/pdi-iniciar`; `/pdi-status` também informa o próximo passo quando não há ciclo ativo.

Sem chat, `python3 scripts/pdi.py onboarding --format text` consulta a orientação. A CLI não interpreta suas respostas: o assistente as registra em notas/propostas e aplica apenas o que foi autorizado. Veja o [guia](docs/user-guide.md).

## Conectar um `outtie` anterior

O comando `connect` com o caminho escolhido confirma a utilização desse espaço. Informar apenas `--outtie CAMINHO setup` não confirma o uso de um estado existente que ainda não está conectado.

```bash
python3 scripts/pdi.py --outtie /home/SEU_USUARIO/espaco-anterior connect
```

Se já houver outro conectado, use `--switch` depois de revisar os destinos. O script não apaga os espaços antigos. Espaços sem `metadata.json` não são assumidos compatíveis: importar seus documentos em novo espaço e preservar originais.

## Workspace com duas raízes

```bash
python3 scripts/pdi.py --outtie ../outtie connect
code .local/pdi.code-workspace
```

Setup e connect incluem innie e o destino real do outtie no workspace local por padrão. Esse arquivo não é versionado e funciona também com destinos personalizados. O `pdi.code-workspace` da raiz abre Innie e Outtie pelo link `pessoal`; prefira o workspace local se a integração tiver dificuldade com symlinks. Os dados continuam fisicamente no outtie. Para abrir somente innie no workspace local, use `setup --no-two-roots` ou `connect --no-two-roots`; `--two-roots` continua aceito.

## Atualizações

Atualizar o clone pelo Git preservando mudanças locais e conferir `doctor` novamente. Dados pessoais permanecem no outtie. Publicação e revisão de fontes são tarefas do mantenedor: veja [manutenção](docs/maintenance.md). Remotes individuais são opcionais e escolhidos pelo usuário.
