# Contrato específico

**Ativa quando:** começar, continuar ou conectar um estado anterior. **Entradas:** configuração local, perfil e lista de ciclos. **Passos:** verificar instalação; detectar novo/existente; confirmar perfil e ciclo; pedir somente o mínimo faltante; selecionar importação ou diagnóstico. **Saídas:** resumo de contexto e proposta de preenchimento inicial. **Aceitação:** uma nova sessão consegue localizar o plano vigente; não cria um novo ciclo por engano. **Limite:** não migra estado incompatível sem o fluxo específico de recuperação.

## Operação local

Executar `python3 scripts/pdi.py doctor`; ler `python3 scripts/pdi.py state`. Se não houver espaço, orientar `setup`. Confirmar perfil e calendário com perguntas curtas.

As verificações semânticas dependem do assistente e da revisão humana; o CLI protege estrutura e persistência.
