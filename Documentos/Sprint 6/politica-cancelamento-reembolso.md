# Política de cancelamento e reembolso

## Por que esta política existe

Na análise de impactos negativos, o grupo apontou que plataformas costumam jogar o risco de cancelamentos em cima do artista (item 4, "Vulnerabilidade operacional e ausência de proteção"). Esta política divide esse risco de forma justa e define o que acontece com o valor retido em cada caso. Ela usa os status que já existem no banco: contrato `cancelado` e pagamento `reembolsado` ou `liberado`.

## Cancelamento pelo cliente

Quanto mais perto do evento, maior a parte que fica com o artista, porque fica mais difícil ele conseguir outro trabalho para a mesma data.

| Antecedência do cancelamento | Reembolso ao cliente | Fica com o artista |
|---|---|---|
| 30 dias ou mais | 100% | 0% |
| De 15 a 29 dias | 70% | 30% |
| De 7 a 14 dias | 50% | 50% |
| Menos de 7 dias | 0% | 100% |

O cliente também pode cancelar sem custo até 24 horas depois de aceitar a proposta, desde que o evento esteja a mais de 7 dias.

## Cancelamento pelo artista

- O cliente recebe **100% de reembolso**, sempre.
- A plataforma reabre o pedido de orçamento com prioridade para outros artistas da mesma categoria.
- **Consequências para o artista:**
  - 1º cancelamento em 12 meses: advertência no painel.
  - 2º cancelamento em 12 meses: suspensão de 30 dias na busca.
  - Cancelamento com menos de 7 dias de antecedência conta como dois.
- Cancelamentos por motivo de força maior (abaixo) não contam.

## Não comparecimento

- **Artista não compareceu:** reembolso de 100% ao cliente, que pode avaliar o artista mesmo sem o evento ter sido concluído. Conta como cancelamento com menos de 7 dias.
- **Cliente não estava no local ou impediu a apresentação:** o valor é liberado ao artista, desde que ele comprove que compareceu (foto no local, mensagem no horário combinado).

## Mudança de data

Remarcar não é cancelar. Se o pedido de mudança for feito com 15 dias ou mais de antecedência e a outra parte aceitar (usando a contraproposta de data), não há custo. Com menos de 15 dias, a remarcação depende do aceite do artista, que pode cobrar a diferença combinada entre os dois.

## Força maior

Situações fora do controle das partes, como evento climático extremo, doença com atestado médico, falecimento na família ou interdição do local pelo poder público. Nesses casos, a parte afetada envia a comprovação pela plataforma, e a equipe analisa em até 48 horas. As opções são:

1. remarcar sem multa para uma data em até 6 meses; ou
2. reembolso integral ao cliente, sem penalidade para nenhum dos lados.

## Contestação depois do evento

- O cliente tem até **48 horas após a data do evento** para contestar (atraso grave, serviço diferente do combinado).
- Durante a contestação, o valor continua retido e a plataforma faz a mediação em até 5 dias úteis.
- Sem contestação no prazo, o valor é liberado automaticamente ao artista.

## Prazos de reembolso

O reembolso é feito pelo mesmo meio de pagamento em até 7 dias úteis depois do cancelamento ou da decisão da mediação.

## Como isso aparece no sistema

| Situação | Contrato | Pagamento |
|---|---|---|
| Evento confirmado pelo cliente | concluido | liberado |
| Cancelamento com reembolso total | cancelado | reembolsado |
| Cancelamento com reembolso parcial | cancelado | reembolsado (valor devolvido) e liberado (parte do artista) |
| Contestação em andamento | valor_retido | retido |
