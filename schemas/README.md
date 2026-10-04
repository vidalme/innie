# Schemas de referência

JSON Schema Draft 2020-12, sem instalação obrigatória de validador externo. Descrevem o estado e operações. O runtime utiliza `model.validate` e `apply_operations` para referências, datas, ciclos ativos, dependências, campos quantitativos e autorização. Um schema estrutural aprovado isoladamente não garante a validade semântica.

Alteração incompatível exige nova versão e migração explícita. O comando migrate atual apenas reconhece a versão 1; nunca converte arquivos desconhecidos silenciosamente.

A correção de desconhecidos amplia a leitura do schema 1 para aceitar `effort_hours: null` e fuso desconhecido, conforme o contrato de dados. O código atual continua lendo os estados anteriores sem convertê-los. Executáveis antigos que rejeitavam esses nulls não devem ser usados para abrir estados novos; o retorno a uma versão antiga exige restaurar um backup compatível em outro destino.
