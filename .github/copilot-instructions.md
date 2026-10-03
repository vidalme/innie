# Copilot — ponto de entrada

Aplicar o [contrato geral](../AGENTS.md). Oferecer o agente `copiloto-desenvolvimento` para o uso cotidiano e consultar [knowledge/index.json](../knowledge/index.json) quando houver dúvida institucional.

O estado está no `outtie`, acessível por `pessoal`. Recuperar a revisão atual com `python3 scripts/pdi.py state`. Não inventar contexto se o acesso falhar. As skills em `.github/skills` descrevem os procedimentos; os prompts em `.github/prompts` fornecem atalhos opcionais.

Usar `proposal/apply` para mudanças, `render` para visões e `export` para textos do Team Guide. Respeitar revisão do usuário e não alterar arquivos canônicos diretamente. Sem ferramenta de execução, devolver uma proposta documentada e explicar como aplicá-la.

Não presumir intervalo mínimo de 12 meses entre promoções; a regra não foi confirmada. Não prometer promoção, posição 9box ou validade institucional de uma evidência.
