-- View: metropolitana_estadistica_departamento

-- DROP VIEW metropolitana_estadistica_departamento;

CREATE OR REPLACE VIEW metropolitana_estadistica_departamento AS 
 SELECT row_number() OVER () AS id,
    metropolitana_estadistica.ano,
    metropolitana_estadistica.mes,
    metropolitana_estadistica.ciclo,
    metropolitana_estadistica.iddepartamento,
    sum(metropolitana_estadistica.total) AS total,
    sum(metropolitana_estadistica.entregados) AS entregados,
    sum(metropolitana_estadistica.pendientes) AS pendientes,
    (btrim(to_char(metropolitana_estadistica.ciclo, '00'::text)) || btrim(to_char(metropolitana_estadistica.mes, '00'::text))) || "right"(metropolitana_estadistica.ano::character varying::text, 2) AS estadisticaciclo_id
   FROM metropolitana_estadistica
  GROUP BY metropolitana_estadistica.ano, metropolitana_estadistica.mes, metropolitana_estadistica.ciclo, metropolitana_estadistica.iddepartamento;

ALTER TABLE metropolitana_estadistica_departamento
  OWNER TO postgres;

-- Rule: metropolitana_estadistica_departamento_delete ON metropolitana_estadistica_departamento

-- DROP RULE metropolitana_estadistica_departamento_delete ON metropolitana_estadistica_departamento;

CREATE OR REPLACE RULE metropolitana_estadistica_departamento_delete AS
    ON DELETE TO metropolitana_estadistica_departamento DO INSTEAD NOTHING;

