# Instalação e primeiro uso — Windows / Ubuntu WSL2

## Pré-requisitos

Windows com WSL2 Ubuntu, VS Code, extensão WSL e Copilot autorizado. Python 3.11 ou superior e Git dentro do Ubuntu. A CLI utiliza somente a biblioteca padrão; não precisa de pip, API key ou venv. Poppler é opcional para extrair texto de PDF.

Verificar a distribuição no PowerShell: `wsl --list --verbose`. Se a distribuição não existir ou não estiver em versão 2, seguir [documentação oficial WSL](https://learn.microsoft.com/windows/wsl/install). O script opcional `scripts/windows-prepare.ps1` oferece `-InstallWSL` e `-InstallVSCode`; pode exigir privilégios e reinício. Ele não instala credenciais Copilot nem configura contas.

## 1. Copiar os arquivos

Extrair o ZIP em local temporário e copiar as duas pastas irmãs para o filesystem Linux, por exemplo `~/pdi-copilot/innie` e `~/pdi-copilot/outtie`. Não copiar uma pasta dentro da outra. Não incluir `.git` de outro projeto. Os ZIPs distribuídos não contêm Git interno nem symlink pré-criado.

## 2. Preparar

No Ubuntu:

```bash
cd ~/pdi-copilot/innie
python3 --version
python3 scripts/pdi.py setup
python3 scripts/pdi.py doctor
code pdi.code-workspace
```

Se Python/Git/Poppler estiverem ausentes, o instalador opcional executa apt somente com a flag explícita:

```bash
bash scripts/install.sh --install-deps
```

Sem essa flag, `bash scripts/install.sh` apenas prepara o espaço. Para escolher outro destino: `bash scripts/install.sh --outtie ../meu-outtie`. Instalação não publica arquivos.

## 3. Conferir o Copilot

Confirmar que a janela do VS Code mostra conexão ao Ubuntu/WSL e a conta Copilot está autenticada. Abrir as customizações de chat e verificar agente `copiloto-desenvolvimento`, catorze skills e prompts `pdi-*`. O local da interface pode variar conforme versão.

Selecionar o assistente e pedir: “Leia minha revisão atual, informe ciclo ativo e não modifique nada”. A resposta deve coincidir com `python3 scripts/pdi.py state`. Se não conseguir ler, seguir troubleshooting, usando caminhos explícitos e alternativa de duas raízes. O doctor testa filesystem, não o contexto do modelo.

## 4. Primeiro plano

Informar cargo/senioridade, área, objetivo, disponibilidade e datas reais. Anexar ou importar avaliação anterior, matriz técnica e PDI parcial. Os documentos pessoais entram no `outtie`; nunca em knowledge. O assistente prepara diagnóstico e proposta. Revisar antes de aplicar compromissos.

## Conectar um `outtie` anterior

```bash
python3 scripts/pdi.py --outtie /home/SEU_USUARIO/espaco-anterior connect
```

Se já houver outro conectado, use `--switch` depois de revisar os destinos. O script não apaga os espaços antigos. Espaços sem `metadata.json` não são assumidos compatíveis: importar seus documentos em novo espaço e preservar originais.

## Alternativa com duas raízes

```bash
python3 scripts/pdi.py --outtie ../outtie connect --two-roots
code .local/pdi.code-workspace
```

O workspace local abre innie e outtie e não é versionado. Os dados continuam fisicamente no outtie; não há duplicação. Na instalação padrão use `pdi.code-workspace` da raiz ou o workspace retornado pelo setup.

## Instalação a partir de Git

Depois de publicar o núcleo no repositório autorizado, clonar com Git ou `scripts/acquire.py --innie-url URL --destination CAMINHO`. O script só clona; autenticação é feita pelo Git corporativo. Preparar um outtie local com setup. Remotes individuais são opcionais e escolhidos pelo usuário.
