# Propostas de mudança

## Fluxo

1. Ler state e sua revisão.
2. Criar arquivo JSON de operações dentro da inbox.
3. Executar proposal, que valida e gera proposta na revisão corrente.
4. Mostrar ao usuário o que mudará, por quê, evidências e efeito no cronograma.
5. Aplicar com approve quando a revisão estiver autorizada; executar render.

```bash
python3 scripts/pdi.py proposal --changes pessoal/inbox/mudancas.json --reason "Plano revisado na P2P"
python3 scripts/pdi.py apply --proposal pessoal/proposals/ID_RETORNADO.json --approve
python3 scripts/pdi.py render
```

O argumento changes aponta para uma lista JSON. A proposta gerada contém id, expected_revision, created_at, reason e operations. Aprovação não representa validação institucional. Proposta stale falha; refazer com contexto atual. Não aplicar modificando o campo expected_revision manualmente.

## Operações suportadas

| op | Campos | Uso |
| --- | --- | --- |
| profile | value objeto | Preencher/atualizar perfil |
| calendar | cycle_id e value objeto | Atualizar datas, label, milestones e confirmação da política |
| upsert | collection, value e cycle_id opcional | Inserir ou atualizar registro por ID |

Collections globais: sources, evidence. Collections de ciclo: objectives, actions, criterion_assessments, competency_assessments, metrics, events. Sem cycle_id, usa ciclo ativo. Upsert preserva campos não enviados; para desconhecido enviar null. Exclusão não é suportada. Cancelamento é status com justificativa e revisão, não delete.

## Exemplo fictício completo

O arquivo `templates/example-changes.json` ilustra criação de objetivo e ação; substitua com dados revisados. Existe ciclo ativo antes de aplicar.

```json
[
  {"op":"profile","value":{"seniority":"Júnior","weekly_capacity_hours":2}},
  {"op":"upsert","collection":"objectives","value":{"id":"obj-comunicacao","title":"Melhorar comunicação de resultados","description":"Relatos concisos e úteis ao time"}},
  {"op":"upsert","collection":"actions","value":{"id":"action-oficina","title":"Preparar oficina de um problema recorrente","status":"planned","description":"Preparar material e conduzir sessão, após alinhamento do público e agenda.","effort_hours":5,"objective_ids":["obj-comunicacao"],"criterion_ids":["CI-06"],"evidence_ids":[],"source_ids":[],"depends_on":[]}}
]
```

Sem prazo informado a ação continua com prazo pendente; o sistema não inventa dia institucional. Uma oficina só será relacionada a CI-07 se duração e condições forem comprovadas.

## Revisão de evidência

Importar arquivo, obter source_id e propor evidence. Relacionar evidence_id à ação. Usar verification claimed inicialmente quando só houver relato. Para uma confirmação institucional, incluir confirmation_source. O conteúdo do arquivo precisa ser lido para elevar a classificação.

## Compatibilidade e integridade

Não inventar IDs de fonte. Operações que referenciam IDs inexistentes falham. Uma aplicação aceita várias operações relacionadas, validadas juntas, permitindo criar objetivo e ação no mesmo lote. Arquivos de origem ficam preservados mesmo se interpretação posterior falhar. O backup é a recuperação principal de perda do ambiente, não um rollback por edição de snapshots.
