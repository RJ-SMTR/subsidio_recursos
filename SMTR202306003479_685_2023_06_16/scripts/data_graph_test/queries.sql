-- Pré-soluçao:

SELECT
  *
FROM
  `rj-smtr.projeto_subsidio_sppo.viagem_conformidade`
WHERE
  DATA = "2023-03-01"
  AND servico_informado = "010"
  AND datetime_partida > "2023-03-01 22:00:00"
ORDER BY
  datetime_partida;

-- ==> shape_pre
SELECT
  shape_id,
  shape,
  start_pt,
  end_pt
FROM
  `rj-smtr.projeto_subsidio_sppo.viagem_planejada`
WHERE
  DATA = "2023-03-01"
  AND servico = '010';

-- ==> gps_pre
SELECT
  id_veiculo,
  servico_informado as servico,
  timestamp_gps,
  posicao_veiculo_geo,
  status_viagem
FROM
  `rj-smtr-dev.SMTR_010_01_03_2023.registros_status_viagem`
WHERE
  DATA = "2023-03-01"
  AND servico_informado = '010'
  AND timestamp_gps BETWEEN "2023-03-01T22:35:15"
  AND "2023-03-01T22:59:51";

-- Pós-solução:

SELECT
  *
FROM
  `rj-smtr-dev.SMTR202212006611_reprocessamento.viagem_conformidade`
WHERE
  DATA = "2023-03-01"
  AND servico_informado = "010"
  AND datetime_partida > "2023-03-01 22:00:00"
ORDER BY
  datetime_partida;

-- ==> shape_pos
SELECT
  shape_id,
  shape,
  start_pt,
  end_pt
FROM
  `rj-smtr-dev.SMTR202212006611_reprocessamento.viagem_planejada`
WHERE
  DATA = "2023-03-01"
  AND servico = '010';

-- ==> gps_pos
SELECT
  id_veiculo,
  servico_informado as servico,
  timestamp_gps,
  posicao_veiculo_geo,
  status_viagem
FROM
  `rj-smtr-dev.SMTR202212006611_reprocessamento.registros_status_viagem`
WHERE
  DATA = "2023-03-01"
  AND servico_informado = '010'
  AND timestamp_gps BETWEEN "2023-03-01T22:35:15"
  AND "2023-03-01T22:59:51";
