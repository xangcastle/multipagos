-- View: entrega_diaria

-- DROP VIEW entrega_diaria;

CREATE OR REPLACE VIEW entrega_diaria AS 
 SELECT row_number() OVER () AS id,
    pdatos.dia,
    pdatos.username,
    pdatos.departamento,
    sum(pdatos.entregas) AS entregas,
    sum(pdatos.rezago) AS rezago
   FROM ( SELECT date_trunc('day'::text, p.fecha_entrega) AS dia,
            ( SELECT auth_user.username
                   FROM auth_user
                  WHERE auth_user.id = p.user_id) AS username,
            ( SELECT metropolitana_departamento.name
                   FROM metropolitana_departamento
                  WHERE metropolitana_departamento.id = p.iddepartamento) AS departamento,
            count(*) AS entregas,
            0 AS rezago
           FROM metropolitana_paquete p
          WHERE p.fecha_entrega IS NOT NULL AND p.estado::text = 'ENTREGADO'::text
          GROUP BY date_trunc('day'::text, p.fecha_entrega), p.user_id, p.iddepartamento
        UNION
         SELECT date_trunc('day'::text, p.fecha_entrega) AS dia,
            ( SELECT auth_user.username
                   FROM auth_user
                  WHERE auth_user.id = p.user_id) AS username,
            ( SELECT metropolitana_departamento.name
                   FROM metropolitana_departamento
                  WHERE metropolitana_departamento.id = p.iddepartamento) AS departamento,
            0 AS entregas,
            count(*) AS rezago
           FROM metropolitana_paquete p
          WHERE p.fecha_entrega IS NOT NULL AND p.estado::text = 'REZAGADO'::text
          GROUP BY date_trunc('day'::text, p.fecha_entrega), p.user_id, p.iddepartamento) pdatos
  GROUP BY pdatos.dia, pdatos.username, pdatos.departamento;

ALTER TABLE entrega_diaria
  OWNER TO postgres;
