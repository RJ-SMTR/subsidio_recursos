# Recurso: SMTR202212006620

---

## Contexto

**Solicitação**: "Bom dia, Solicitamos a verificação do itinerário da linha 663, por ser uma linha do tipo circular e com 2 pontos finais, verificamos que diversas viagens não estão sendo apuradas, solicitamos a verificação do itinerário".

**Linha afetada**: 663

**Período**: 01/06/2022 até 31/12/2022

## Resumo

### Problema

Todas as viagens do ano de 2023 presentes na amostra analisada foram identificadas. 

Para os casos das viagens não identificadas, todas do ano de 2022, as explicações encontradas foram:

1) O solicitante compreendeu que o serviço realizou duas viagens de ida e volta, quando na verdade ocorreu apenas uma viagem.

Exemplo com o caso do veículo B28514 na manhã do dia 27/09/2022:

No gabarito, foi indicado que o veículo teria feito duas viagens nos seguintes intervalos:
- Entre 05:50 e 05:46
- Entre 06:51 e 07:39

A primeira viagem foi identificada como iniciada às 05:51 e terminou às 07:37, horário que abrange as duas viagens acima.

Viagem identificada (viagem circular): 

<img src="./data/figures/663_identificada.png" width="800">

Se filtrarmos o intervalo da viagem da amostra não identificada, ela retorna os sinais de GPS apenas em um sentido:

<img src="./data/figures/viagens_n_encontradas_663.png" width="800">



2) Em três casos da amostra, a viagem não foi identificada:

- B28631 no dia 14/09/2022 entre 06:16 e 07:13
- B28514 no dia 22/09/2022 entre 05:46 e 06:35
- B28631 no dia 22/09/2022 entre 06:14 e 07:04

<img src="./data/figures/viagens_n_encontradas_663.png



### Resultado


> **Status: Finalizada **.

**Valor a pagar: Não se aplica**

## Análise exploratória

O que explica a variação no POD? Mudança no shape em janeiro?

<img src="./data/figures/pod_663.png" width="800">


Das 24 viagens recebidas na amostra, duas eram casos de viagens dos mesmos veículos que ocorriam em horários e dias sobrepostos, logo foram desconsideradas na análise.

Quanto às 22 viagens restantes:
- 13 foram identificadas com os dados de viagens apuradas.
- 5 são inválidas, pois são viagens duplicadas quando na verdade a linha é circular.
- 1 o veículo fez apenas metade do trajeto
- 3 viagens não foram identificadas, mas os veículos emitiram sinais de GPS. 


### Método de avaliação da amostra

A comparação entre o `datetime_partida` do gabarito e da solução foi feita com uma margem de 10 minutos para mais ou para menos.

