# Recurso: SMTR202211008775

**Solicitação**:
"Bom dia. Solicito a verificação do sistema do desenho e localização dos pontos da linha 844. Ocorre que desde o inicio da avaliação das viagens esta linha nunca consegue que a apuração da SMTR atinja o planejado, mas a empresa opera a linha conforme os parâmetros estabelecidos pela SMTR. Parece ser alguma falha sistêmica, pois a linha é muito curta, ligando o Jardim Oceânico a Barrinha. Obrigado.".

**Linha afetada**: 844

**Período**: 01/06/2022 até 31/12/2022


--------

### <ins>**Sumário Executivo**</ins>

<br>

**1 - Problema encontrado**: Foi identificado um aumento na quilometragem apurada a partir de 01/01/2023, mesma data em que houve a alteração no ponto de início e de término das viagens do shape.


**2 - Solução proposta**: Reprocessamento das viagens entre 01/06/2022 e 31/12/2022, utilizando o shape de 01/01/2023.

**3 - Resultado**:

Ver a tabela SMTR202211008775_reprocessamento onde foi feito o reprocessamento.

- A quilometragem total das viagens completas aumentou de 13.033 km para 22.122 km, um aumento de 69,73%.

- A quantidade de viagens completas aumentou de 1.920 para 3.258 viagens após o reprocessamento.

- O valor do subsídio a ser pago subiu de R$ 5.237,70 para R$ 38.162,45

<br>

### 1) Análise exploratória

Foi identificada uma alteração no shape em 01/01/2023 que impactou positivamente no POD, já que a quilometragem apurada passou a ser maior devido ao maior número de viagens identificadas.


<img src="./data/output/imagem_problema_844.png" alt="Descrição da imagem" width="800"/>


### 2) Teste amostral

A amostra recebida contem 280 viagens para os dias 15, 20 e 28 de setembro de 2022 e 06, 11 e 19 de julho de 2023, com um total de 136 viagens para 2022 e 144 viagens para 2023.

Ao comparar os dados das viagens completas em produção com os dados do gabarito, nota-se que:

1. O que os consórcios consideram como sendo duas viagens (ida e volta), consideramos como sendo viagens circulares.

2. Segundo os dados do gabarito cada dia teve em média 46 viagens. Se considerarmos que estas viagens são circulares e estão sendo consideradas como ida e volta, então deveríamos ter 23 viagens em média para cada dia.

3. Para os dias de 2023 da amostra, foram encontras em média 23 viagens nas viagens completas.

<img src="./data/output/viagens_2023_producao_gabarito.png" alt="Descrição da imagem" width="800"/>



4. Para 2022 foram encontradas em média apenas 8 viagens por dia nos dados de viagens completas.


<img src="./data/output/viagens_2022_producao_gabarito.png" alt="Descrição da imagem" width="800"/>



### 3) Análise do Reprocessamento

A solução proposta foi o reprocessamento dos dados de 2022 com o shape de 01/01/2023. 

<img src="./data/output/comparacao_solucao_vs_gabarito_2022.png" alt="Descrição da imagem" width="800"/>

Com o reprocessamento, foram identificadas em média 20 viagens para cada um dos dias de 2022.

- Resultados do Reprocessamento:


<img src="./data/output/km_apurada_844.png" alt="Descrição da imagem" width="800"/>


<img src="./data/output/qtd_viagens_844.png" alt="Descrição da imagem" width="800"/>


<img src="./data/output/valor_subsidio_844.png" alt="Descrição da imagem" width="800"/>

<img src="./data/output/POD_844.png" alt="Descrição da imagem" width="800"/>



#### Resultados do reprocessamento:

- A quantidade de viagens completas aumentou de 1.920 para 3.258 viagens após o reprocessamento.

- A quilometragem total das viagens completas aumentou de 13.033 km para 22.122 km, um aumento de 69,73%.

- O valor do subsídio a ser pago subiu de R\$ 5.237,70 para R\$ 38.162,45
