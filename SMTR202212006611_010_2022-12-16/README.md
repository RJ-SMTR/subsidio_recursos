# Recurso: SMTR202211008775

**Mensagem**:
"Bom dia, Solicitamos a verificação do itinerário da linha 010, por ser uma linha do tipo circular e com 2 pontos finais, verificamos que diversas viagens não estão sendo apuradas, solicitamos a verificação".

**Linha afetada**: 010

**Período**: 01/06/2022 até 31/05/2023

-------
### 1) Análise exploratória

Após a análise do trajeto para a primeira quinzena de janeiro de 2023, foi identificada uma inconsistência em que alguns sinais de GPS foram descartados no trecho em "laço" (ver figura abaixo).


![Imagem local](./data/output/figura_1.png)

Ao considerar o shape de 01/06/2023, que divide a viagem circular em ida e volta, os sinais de GPS foram devidamente identificados:

![Imagem local](./data/output/figura_2.png)




### 2) Teste amostral

A partir da alteração do shape, os dados da primeira quinzena de janeiro de 2023 foram reprocessados e comparados com os dados do gabarito enviado pelo consórcio operacional (dados disponíveis [aqui](https://docs.google.com/spreadsheets/d/11jKNeWoXB4Uke4WWwWsjHo8I-ZRr8f3Y/edit#gid=1849603428)).

Método:

A comparação entre o `datetime_partida` do gabarito e da solução foi feita com uma margem de 10 minutos para mais ou para menos. 

Para as viagens não encontradas na etapa anterior, foi verificado se os veículos operaram nos dias e horários apontados no gabarito, com base em dados de GPS e do reprocessamento de conformidade das viagens proveniente do dataset `rj-smtr-dev.20230818_projeto_subsidio_sppo_010`

Resultado do teste:

- Foram identificadas 699 das 706 viagens do gabarito (99%) em um intervalo de + ou - 10 minutos entre os `datetime_partida` do gabarito e da solução.

- Sobre as sete viagens não identificadas: 
    1) Em três casos os veículos não emitiram sinais de GPS no horário indicado no gabarito.
    2) Em dois casos os veículos operaram em outro serviço no horário indicado no gabarito (serviço 007).
    3) Em dois casos a viagem ocorreu, mas ficou um pouco acima da margem de + ou - 10 minutos



### 3) Análise do Reprocessamento

O reprocessamento seguindo os critérios acima para o período entre 01/06/2022 e 31/05/2023 está disponível no dataset `rj-smtr-dev.SMTR202212006611_reprocessamento`.

CONTINUAR DAQUI!!!!
Recalcular o valor a ser pago (tanto nos comentários no notebook quanto nos arquivos finais).
INCLUIR FIGURAS E VALORES TOTAIS



Comparar valores pré e pós reprocessamento segundo as seguintes variáveis:
- A quantidade de viagens completas
- Quilometragem total de viagens completas
- Valor do subsídio a ser pago
- Explicações pontuais sobre os resultados encontrados

Sobre o período entre 01/06/2022 e 31/05/2023:

1) A linha 010 não teve viagens planejadas no mês de junho de 2022.

2) A quilometragem total das viagens completas aumentou de 66.790,1 km para 81.485,2 km, um aumento de 22% após o reprocessamento.

3) A quantidade de viagens identificadas aumentou de 6.414 para 15.670 viagens.

4) O valor do subsídio antes do reprocessamento era de R$ 100.756,68 e após o reprocessamento foi de R$ 135.630,25.

5) Foi identificada uma inconsistência em abril e maio de 2023, em que foram indentificadas mais viagens, mas o POD diário diminuiu, resultando em um pagamento de subsídio menor em relação ao valor do pré-reprocessamento.












