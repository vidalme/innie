# Schemas de referência

JSON Schema Draft 2020-12, sem instalação obrigatória de validador externo. Descrevem o estado e operações. O runtime utiliza `model.validate` e `apply_operations` para referências, datas, ciclos ativos, dependências, campos quantitativos e autorização. Um schema estrutural aprovado isoladamente não garante a validade semântica.

Alteração incompatível exige nova versão e migração explícita. O comando migrate atual apenas reconhece a versão 1; nunca converte arquivos desconhecidos silenciosamente.
