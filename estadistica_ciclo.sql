-- View: metropolitana_estadistica_ciclo

-- DROP VIEW metropolitana_estadistica_ciclo;

CREATE OR REPLACE VIEW metropolitana_estadistica_ciclo AS 
 SELECT (btrim(to_char(metropolitana_estadistica.ciclo, '00'::text)) || btrim(to_char(metropolitana_estadistica.mes, '00'::text))) || "right"(metropolitana_estadistica.ano::character varying::text, 2) AS code,
    metropolitana_estadistica.ano,
    metropolitana_estadistica.mes,
    metropolitana_estadistica.ciclo,
    sum(metropolitana_estadistica.total) AS total,
    sum(metropolitana_estadistica.entregados) AS entregados,
    sum(metropolitana_estadistica.pendientes) AS pendientes
   FROM metropolitana_estadistica
  GROUP BY metropolitana_estadistica.ano, metropolitana_estadistica.mes, metropolitana_estadistica.ciclo;

ALTER TABLE metropolitana_estadistica_ciclo
  OWNER TO postgres;

-- Rule: metropolitana_estadistica_ciclo_delete ON metropolitana_estadistica_ciclo

-- DROP RULE metropolitana_estadistica_ciclo_delete ON metropolitana_estadistica_ciclo;

CREATE OR REPLACE RULE metropolitana_estadistica_ciclo_delete AS
    ON DELETE TO metropolitana_estadistica_ciclo DO INSTEAD NOTHING;

