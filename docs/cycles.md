# Ciclos, entrada parcial e recuperação

## Calendário

Não há ciclo real pré-configurado. Informar início/fim, corte das evidências, fechamento do PDI, avaliação e marcos. O mês da avaliação não determina todos esses campos. O plano acompanha tempo residual mesmo quando o ciclo é encurtado para ajuste institucional.

Ativar exige datas concretas suficientes. Se só houver mês conhecido, manter draft e elaborar cenário provisório. A configuração aceita marcos trimestrais e período final parcial. O assistente propõe marcos; a CLI valida suas datas, sem declarar que são oficiais.

## Ingresso no meio do ciclo

1. Importar exportação do PDI e avaliação.
2. Revisar quais ações pertencem ao ciclo e preservar IDs externos.
3. Criar baseline usando as fontes originais e ações com estado/prévias reais.
4. Distinguir realizado, pendente, desconhecido e atrasado.
5. Planejar apenas o período restante.

Datas futuras em previsão de uma ação done podem significar conclusão antecipada; confirmar completed_on. Não retroagir a criação de novas ações nem usar a reescrita para ocultar atrasos. Referências a trabalho de ciclo anterior ficam históricas.

## Fechamento

Preparar status, painel, plano e comprovações; revisar pendências; executar close aprovado. O archive contém ciclo, perfil de fechamento, evidências/fontes selecionadas, materiais locais, outputs e knowledge usados, além de manifesto de hashes. Links externos não baixados continuam dependentes de acesso.

O rótulo contém início/fim e ID. Reexecução após sucesso não duplica. Se uma falha ocorrer após criar archive e antes de publicar a revisão, a reexecução só retoma quando o arquivo corresponde à revisão fonte. Divergência exige inspeção, nunca sobrescrita.

## Novo ciclo e transferências

Create gera draft com coleções vazias. O perfil atual permanece; avaliações recentes entram como novas fontes/baseline. Não herdar percentuais, elegibilidade, box ou prazos sem revisão. Ações pendentes transferidas ganham ID novo e referência à origem; não levam resultados como se fossem novos. Origem arquivada permanece intacta.

## Resultado tardio

Usar cycle adendum para catalogar uma avaliação ou decisão recebida após fechamento. O adendo é registrado no estado atual e referencia fonte preservada, fora do archive. O snapshot e manifesto originais não mudam. O assistente pode resumir esse adendo ao planejar o ciclo novo.

## Backup, restauração e formato antigo

Backup do espaço real, fora dele, guarda revisões, arquivos e estado. Restore verifica o manifesto e exige destino novo. Após restaurar, conectar com --switch. Copiar somente innie ou symlinks não salva o outtie.

Para outtie sem metadata/schema reconhecido, preservar a pasta antiga, criar outra e importar documentos. A versão 0.1 não implementa migração arbitrária de históricos; recusa essa suposição. O plano prevê adaptadores futuros para formatos conhecidos após existir um caso real de migração.
