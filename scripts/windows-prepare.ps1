<# Preparação opcional do Windows. Executar em PowerShell; instalação exige flags. #>
param([switch]$InstallWSL, [switch]$InstallVSCode)
$ErrorActionPreference = 'Stop'
if ($InstallWSL) {
    wsl --install -d Ubuntu
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar WSL. Verifique privilégios e reinício pendente.' }
}
if ($InstallVSCode) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'winget não encontrado.' }
    winget install --id Microsoft.VisualStudioCode --exact
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar VS Code.' }
}
Write-Host 'Verifique Ubuntu/WSL2 com wsl --list --verbose. A distribuição precisa estar em versão 2.'
Write-Host 'Após instalar/reiniciar, abra Ubuntu, copie o pacote para ~/pdi-copilot e execute o guia INSTALL.md.'
Write-Host 'Copilot requer autenticação/licença e aprovação do workspace; este script não fornece credenciais.'
