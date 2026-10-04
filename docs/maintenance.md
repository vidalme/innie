# Manutenção e publicação

Este documento é para quem mantém e distribui o núcleo. Participantes começam pelo [INSTALL](../INSTALL.md), clonando o repositório já publicado.

## Publicar o núcleo pela primeira vez

Se o núcleo ainda não estiver em Git, inicializar e publicar no serviço autorizado. Não repetir esta inicialização em um clone existente. Manter repositórios separados quando houver versionamento individual. `innie` é interno à empresa porque contém normas institucionais; `outtie` pode permanecer local ou usar um remoto privado permitido.

Depois de copiar e verificar:

```bash
cd ~/pdi-copilot/innie
python3 scripts/pdi.py init-git --scope innie
git status --short
git add .
git commit -m "Implement copiloto PDI initial pilot"
git remote add origin URL_DO_REPOSITORIO_INTERNO
git push -u origin main
```

Conferir que pessoal e .local não aparecem rastreados. Em caso de arquivo individual já rastreado, não basta adicionar ignore: tratar índice/histórico com quem administra o repositório. Não publicar o pacote em repositório aberto.

Para Git individual, executar init-git no escopo outtie e fazer commit/remote/push dentro do outtie, escolhendo conscientemente documentos rastreados. Esta é decisão do usuário; scripts não publicam remotamente.

## Atualizar o núcleo

Fazer backup individual e atualizar innie pelo Git. Reexecutar doctor. Se regras/versão mudarem, pedir revisão do plano ativo. Nada reinterpreta archives automaticamente. Mudanças locais no código são discutidas/commitadas separadamente dos dados individuais.

## Atualizar normas

Adicionar fonte institucional e proveniência, registrar escopo/vigência, extrair diferenças e confirmar com gestor/RH. Atualizar catalog, valuation, competências e guia de evidências sem incluir anotações individuais. Registrar a decisão em knowledge/validation-decisions e CHANGELOG. Não mudar a regra de intervalo mínimo entre promoções sem texto/confirmacão.

A política atual permite até dois steps em 1C no material fornecido; isso não representa promoção assegurada. Calendário, cálculo técnico, normalização e eventual intervalo mínimo são pendências de validação. Inglês não entra no percentual técnico dos critérios em que é excluído.

## Qualidade

Executar unittest e check_package; revisar os casos manuais no VS Code; usar fixtures sintéticas na CI. Python core não requer dependências de pip. Hooks/CI são verificações auxiliares e não impedem todas as formas de vazamento.

## Gestão do projeto

Um responsável mantém versões e dúvidas. O gestor revisa critérios; o colega piloto fornece feedback de uso. Priorizar problemas observados de onboarding, continuidade e evidência. A documentação original em docs/planning contém objetivos, requisitos RF/RNF, cronograma de quatro semanas e critérios CA. Esta versão concretiza o núcleo e registra limites; futuras versões seguem esse backlog.

## Medir o piloto

Comparar tempo para plano/update/PDI antes e depois, intervenções do criador, frequência de revisão e evidências utilizáveis. Dois participantes não demonstram causalidade sobre promoções da empresa inteira. Preservar resultados e feedback com consentimento para avaliar utilidade do próprio projeto.
