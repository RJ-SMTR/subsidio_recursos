# Recurso: SMTR202212006620

---

## Contexto

**Solicitação**: "Bom dia, Solicitamos a verificação do itinerário da linha 663, por ser uma linha do tipo circular e com 2 pontos finais, verificamos que diversas viagens não estão sendo apuradas, solicitamos a verificação do itinerário".

**Linha afetada**: 663

**Período**: 01/06/2022 até 31/12/2022

## Resumo

### Problema
O solicitante compreendeu que o serviço realizou duas viagens de ida e volta, quando na verdade ocorreu apenas uma viagem. 

### Solução
Não se aplica.

### Resultado

Das 24 viagens recebidas na amostra, 2 eram casos de viagens dos mesmos veículos que ocorriam em horários e dias sobrepostos, logo foram desconsideradas na análise e classificadas como "Viagem duplicada na amostra".

Quanto às 22 viagens restantes:
- 16 viagens foram identificadas com os dados de viagens apuradas e classificadas com o status "Viagem circular identificada e já paga".
- 6 viagens circulares foram consideradas inválidas por não passarem no raio de 500m do ponto inicial ou final, e foram classificadas como "Viagem circular inválida - sem sinal inicial/final dentro do raio de 500m".


> **Status: Finalizado **.

**Valor a pagar: Não se aplica**

## Análise exploratória

O Percentual de Operação Diário (POD) da linha apresentou valores abaixo do mínimo de 80% no ano de 2022.

<img src="./data/figures/pod_663.png" width="800">


1) O solicitante compreendeu que o serviço realizou duas viagens de ida e volta, quando na verdade ocorreu apenas uma viagem.

Exemplo com o caso do veículo B28514 na manhã do dia 27/09/2022:

No gabarito, foi indicado que o veículo teria feito duas viagens nos seguintes intervalos:
- Entre 05:50 e 05:46
- Entre 06:51 e 07:39

A primeira viagem foi identificada como iniciada às 05:51 e terminou às 07:37, horário que abrange as duas viagens acima.

Viagem identificada: 

<img src="./data/figures/663_identificada.png" width="800">


Se filtrarmos o intervalo da viagem da amostra não identificada, ela retorna os sinais de GPS apenas em um sentido:

<img src="./data/figures/663_não_identificada.png" width="800">



### Método de avaliação da amostra

A comparação entre o `datetime_partida` do gabarito e da solução foi feita com uma margem de 10 minutos para mais ou para menos.

