# Regras de pontuação do match de compatibilidade

## Objetivo

O diferencial do ArtConnect é mostrar primeiro os artistas que mais combinam com o evento, em vez de uma lista solta. Este documento define como essa compatibilidade é calculada. As regras estão implementadas no arquivo `artconnect/match.py`.

## Dados que o cliente informa

- Categoria do serviço (DJ, cantor, mágico...): funciona como filtro, só aparecem artistas da categoria escolhida.
- Cidade do evento.
- Orçamento máximo, em reais.
- Data do evento.

Todos são opcionais. Sem cidade, orçamento e data, a busca continua ordenada só pela avaliação, como antes.

## Critérios e pesos

| Critério | Peso | Como pontua |
|---|---|---|
| Preço | 35 | Preço mínimo dentro do orçamento: 35. Até 20% acima do orçamento: 15. Mais de 20% acima: 0. |
| Cidade | 25 | Artista da mesma cidade do evento: 25. Outra cidade: 0. |
| Data | 25 | Artista livre na data: 25. Ocupado (marcou a data na agenda ou já tem contrato nesse dia): 0. |
| Avaliação | 15 | Nota média ÷ 5 × 15. Artista sem avaliação recebe 7,5 (metade), para não ser punido por ser novo. |

## Por que esses pesos

- **Preço (35):** nas entrevistas, o valor foi o primeiro fator citado para desistir de contratar. Os 20% de tolerância existem porque muitos clientes aceitam pagar um pouco mais pelo artista certo.
- **Cidade (25) e Data (25):** são condições práticas. Um artista ocupado ou muito longe dificilmente fecha negócio.
- **Avaliação (15):** pesa menos para não esconder artistas novos, que é um dos impactos positivos que o projeto promete.

## Fórmula

Só entram na conta os critérios que o cliente informou.

- Pontos possíveis = 15 (avaliação) + 35 se informou orçamento + 25 se informou cidade + 25 se informou data.
- Compatibilidade = pontos obtidos ÷ pontos possíveis × 100, arredondada para o inteiro mais próximo (,5 arredonda para cima).

A lista é ordenada pela compatibilidade. Em caso de empate, fica na frente quem tem a maior nota.

## Exemplo calculado

Busca: DJs, em São Paulo, orçamento de R$ 2.500, no dia 05/12/2026. Pontos possíveis: 15 + 35 + 25 + 25 = 100.

| Artista | Preço | Cidade | Data | Avaliação | Total |
|---|---|---|---|---|---|
| Selva Ritmo (SP, R$ 2.400, nota 5,0, ocupado no dia) | 35 | 25 | 0 | 15 | **75%** |
| Neon Sombra (SP, R$ 3.080, sem avaliação, livre) | 0 | 25 | 25 | 7,5 | **58%** |
| Pulso Tropical (Brasília, R$ 2.600, sem avaliação, livre) | 15 | 0 | 25 | 7,5 | **48%** |

Leitura do exemplo: o Neon Sombra passa mais de 20% do orçamento (R$ 3.080 contra o limite de R$ 3.000), então zera no preço. O Pulso Tropical está só 4% acima e ganha 15, mas perde os pontos de cidade. O Selva Ritmo é o mais compatível mesmo estando ocupado, e a tela avisa "ocupado na data" para o cliente saber que vai precisar negociar outro dia.

## Limitações conhecidas

- A cidade é comparada pelo nome. Bairros e cidades vizinhas ainda não contam como "perto".
- O preço usado é o "a partir de" do perfil, não o valor final da proposta.
