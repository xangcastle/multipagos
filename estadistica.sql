-- View: metropolitana_estadistica

-- DROP VIEW metropolitana_estadistica;

CREATE OR REPLACE VIEW metropolitana_estadistica AS 
 SELECT row_number() OVER () AS id,
    data.ano,
    data.mes,
    data.ciclo,
    data.iddepartamento,
    data.idmunicipio,
    data.user_id,
    sum(data.total) AS total,
    sum(data.entregados) AS entregados,
    sum(data.pendientes) AS pendientes
   FROM ( SELECT metropolitana_paquete.ano,
            metropolitana_paquete.mes,
            metropolitana_paquete.ciclo,
            metropolitana_paquete.iddepartamento,
            metropolitana_paquete.idmunicipio,
            metropolitana_paquete.user_id,
            count(*) AS total,
            0 AS entregados,
            0 AS pendientes
           FROM metropolitana_paquete
          GROUP BY metropolitana_paquete.ano, metropolitana_paquete.mes, metropolitana_paquete.ciclo, metropolitana_paquete.iddepartamento, metropolitana_paquete.idmunicipio, metropolitana_paquete.user_id
        UNION
         SELECT metropolitana_paquete.ano,
            metropolitana_paquete.mes,
            metropolitana_paquete.ciclo,
            metropolitana_paquete.iddepartamento,
            metropolitana_paquete.idmunicipio,
            metropolitana_paquete.user_id,
            0 AS total,
            count(*) AS entregados,
            0 AS pendientes
           FROM metropolitana_paquete
          WHERE metropolitana_paquete.entrega = true
          GROUP BY metropolitana_paquete.ano, metropolitana_paquete.mes, metropolitana_paquete.ciclo, metropolitana_paquete.iddepartamento, metropolitana_paquete.idmunicipio, metropolitana_paquete.user_id
        UNION
         SELECT metropolitana_paquete.ano,
            metropolitana_paquete.mes,
            metropolitana_paquete.ciclo,
            metropolitana_paquete.iddepartamento,
            metropolitana_paquete.idmunicipio,
            metropolitana_paquete.user_id,
            0 AS total,
            0 AS entregados,
            count(*) AS pendientes
           FROM metropolitana_paquete
          WHERE metropolitana_paquete.entrega = false
          GROUP BY metropolitana_paquete.ano, metropolitana_paquete.mes, metropolitana_paquete.ciclo, metropolitana_paquete.iddepartamento, metropolitana_paquete.idmunicipio, metropolitana_paquete.user_id) data
  GROUP BY data.ano, data.mes, data.ciclo, data.iddepartamento, data.idmunicipio, data.user_id
  ORDER BY data.ano, data.mes, data.ciclo, data.iddepartamento, data.idmunicipio, data.user_id;

ALTER TABLE metropolitana_estadistica
  OWNER TO postgres;

-- Rule: metropolitana_estadistica_delete ON metropolitana_estadistica

-- DROP RULE metropolitana_estadistica_delete ON metropolitana_estadistica;

CREATE OR REPLACE RULE metropolitana_estadistica_delete AS
    ON DELETE TO metropolitana_estadistica DO INSTEAD NOTHING;

