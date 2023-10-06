# Recurso: SMTR202303002183

**Solicitação**:
"Caros Favor verificar o itinerário da linha LECD50 linha circular que não está abrindo viagem, parece que sistema inseriu um ponto final que não representa a localização real, problema similar a 010, 844. Segue mapa da linha".


**Linha afetada**: LECD50 (ou 605)

**Período**: 01/01/2023 até 31/03/2022


--------

### <ins>**Sumário Executivo**</ins>

<br>


**1 - Problema encontrado**: 

Foi identificada uma queda no POD entre os dias 15 de dezembro de 2022 e 31 de março de 2023. 

Após a verificação das viagens no período, foi constatado que:

- No mês de dezembro ocorreram viagens até o dia 14 e a identificação das viagens ocorreu da forma correta.

- A mudança do shape no dia 01/01/2023 fez com que as viagens não fossem identificadas corretamente. 

- Em janeiro não existiu sinal de GPS para os serviços LECD50 e 605.

- O problema foi percebido a partir de fevereiro de 2023. Inclusive as viagens que constam na tabela de viagens completas não foram devidamente identificadas, contendo apenas metade do trajeto esperado (ver figuras na próxima parte). 

- A amostra recebida não inclui os dias afetados. No aguardo de uma amostra que contemple o período entre 01/01/2023 e 31/03/2023.



**2 - Solução proposta**: 

Aguardando a nova amostra.
<!-- Reprocessar o período afetado (01/01/2023 até 31/03/2023) com o shape de 14/12/2022 da linha LECD50. -->


**3 - Resultado**:


> **Status: Bloqueado**. Aguardando nova amostra com dias dentro do período afetado.

**Valor a pagar: R\$ -**


As viagens que ocorreram nas datas que constam na amostra fora do periodo foram classificadas e estão disponíveis no diretório `data/output/analise_amostra_pre_solucao.xlsx`.

Sobre o intervalo entre dezembro de 2022 e março de 2023, em que o Percentual de Operação Diária caiu, pode-se afirmar que:

- Existiu serviço planejado para a linha LECD50 entre dez/22 e mar/23, mas não para a linha 605.

- Com exceção do mês de janeiro de 2023, foram identificados sinais de GPS para a linha LECD50 no período supracitado. Não foram encontrados sinais para a linha 605 no mesmo período.

- Para o serviço 605, existem viagens planejadas e sinais de GPS apenas a partir de 01/06/2023.

<br>

### 1) Análise exploratória

Foi encontrada uma queda no POD entre dezembro de 2022 e março de 2023:

<img src="./data/figures/LECD50_pod.png" alt="Descrição da imagem" width="800"/>


No final do ano, houve uma mudança no ponto médio do shape:

<img src="./data/figures/mudança_LECD50.png" alt="Descrição da imagem" width="800"/>

Que resultou na identificação incorreta das viagens no período afetado:

<img src="./data/figures/problema_LECD50.png" alt="Descrição da imagem" width="800"/>




### 2) Teste amostral



> **Refazer esta etapa com a nova amostra no período entre janeiro e março de 2023**



<!-- Análise pré-solução:

A amostra recebida contem 104 viagens para os dias 13, 21 e 29 de setembro de 2022 e para os dias 04, 12 e 20 de julho de 2023, todas referentes aos veículos A27684 e A27632.

Ao comparar os dados das viagens completas em produção com os dados do gabarito, nota-se que os consórcios consideram como sendo duas viagens (ida e volta), consideramos como sendo viagens circulares. Ou seja, as 104 viagens que constam na amostra são, na verdade, 52 viagens circulares.

Dessas 52 viagens circulares que constam na amostra:

- 32 viagens já foram pagas;
- 16 casos de viagens em que os veículos emitiram sinais de GPS para outro serviço;
- 2 casos em que a viagem não atendeu ao percentual de conformidade do GPS ou do trajeto; e
- 2 casos em que o sinal de GPS ficou fora do raio de 500m do início ou fim da viagem. -->





### Método de avaliação da amostra

A comparação entre o `datetime_partida` da amostra e da solução foi feita com uma margem de 10 minutos para mais ou para menos.

<!-- Para as viagens não encontradas na etapa anterior, foi verificado se os veículos operaram nos dias e horários apontados no gabarito, com base em dados de GPS e do reprocessamento de conformidade das viagens proveniente do dataset `rj-smtr-dev.20230818_projeto_subsidio_sppo_010`  -->


## Reprocessamento

<!-- O reprocessamento seguindo os critérios acima para o período entre 01/06/2022 e 31/05/2023 está disponível no dataset `rj-smtr-dev.SMTR202212006611_reprocessamento`.

Mesmo antes do reprocessamento, não foram encontradas viagens planejadas da linha 010 no mês de junho de 2022. -->

### Resultados
<!-- 
1) A quilometragem total das viagens completas aumentou de 66.790,1 km para 81.485,2 km, um aumento de 22% após o reprocessamento.

<img src="./data/figures/grafico_010_km.png" width="800">

2) A quantidade de viagens identificadas aumentou de 6.414 para 15.670 viagens. Como as viagens que antes eram circulares foram divididas em duas viagens (ida e volta), era esperado que a quantidade de viagens pelo menos dobrasse, mesmo se nenhuma nova viagem fosse identificada.

<img src="./data/figures/grafico_010_qtd_viagens.png" width="800">

3) O valor do subsídio antes do reprocessamento era de R\$ 100.756,68 e após o reprocessamento foi de R\$ 169.626,86. Vale destacar que o valor do reprocessamento foi calculado sem os descontos por km, ou seja, considerando a liminar que derrubou as glosas.

<img src="./data/figures/grafico_010_subsidio.png" width="800">

4) Por fim, o fato de o reprocessamento ter identificado mais viagens também melhorou o POD do serviço forma geral: -->

<!-- <img src="./data/figures/reprocessamento_pod_comparacao.png" width="800"> -->

