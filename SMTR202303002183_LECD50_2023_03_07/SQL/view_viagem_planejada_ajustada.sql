-- Criar a view de viagem planejada com o shape correto para os serviços 605 e LECD50

CREATE OR REPLACE VIEW `rj-smtr-dev.SMTR202303002183_reprocessamento_planejado.viagem_planejada` AS

WITH 
ReferenceData_I AS (
  SELECT
    shape_id,
    shape_id_planejado,
    data_shape,
    shape,
    sentido_shape,
    start_pt,
    end_pt
  FROM
    `rj-smtr.projeto_subsidio_sppo.viagem_planejada`
  WHERE
    data = DATE '2022-12-30'
    AND servico = 'LECD50'
    AND sentido_shape = 'I'
),

ReferenceData_V AS (
  SELECT
    shape_id,
    shape_id_planejado,
    data_shape,
    shape,
    sentido_shape,
    start_pt,
    end_pt
  FROM
    `rj-smtr.projeto_subsidio_sppo.viagem_planejada`
  WHERE
    data = DATE '2022-12-30'
    AND servico = 'LECD50'
    AND sentido_shape = 'V'
)

SELECT
  vp.data,
  vp.tipo_dia,
  vp.servico,
  vp.vista,
  vp.consorcio,
  vp.sentido,
  vp.distancia_planejada,
  vp.distancia_total_planejada,
  vp.inicio_periodo,
  vp.fim_periodo,
  vp.trip_id_planejado,
  vp.trip_id,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.shape_id, ReferenceData_V.shape_id, vp.shape_id)
    ELSE vp.shape_id
  END AS shape_id,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.shape_id_planejado, ReferenceData_V.shape_id_planejado, vp.shape_id_planejado)
    ELSE vp.shape_id_planejado
  END AS shape_id_planejado,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.data_shape, ReferenceData_V.data_shape, vp.data_shape)
    ELSE vp.data_shape
  END AS data_shape,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.shape, ReferenceData_V.shape, vp.shape)
    ELSE vp.shape
  END AS shape,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.sentido_shape, ReferenceData_V.sentido_shape, vp.sentido_shape)
    ELSE vp.sentido_shape
  END AS sentido_shape,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.start_pt, ReferenceData_V.start_pt, vp.start_pt)
    ELSE vp.start_pt
  END AS start_pt,
  CASE
    WHEN ((vp.data > DATE '2022-12-30' AND vp.servico = 'LECD50') OR (vp.data > DATE '2023-05-31' AND vp.servico = '605'))
      THEN COALESCE(ReferenceData_I.end_pt, ReferenceData_V.end_pt, vp.end_pt)
    ELSE vp.end_pt
  END AS end_pt

FROM
  `rj-smtr.projeto_subsidio_sppo.viagem_planejada` vp
LEFT JOIN
  ReferenceData_I ON vp.sentido_shape = ReferenceData_I.sentido_shape
LEFT JOIN
  ReferenceData_V ON vp.sentido_shape = ReferenceData_V.sentido_shape;
