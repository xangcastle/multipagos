# -*- coding: utf-8 -*-
from metropolitana.models import Paquete
from cartera.models import Gestion
from verificaciones.models import Verificacion
from datetime import datetime
from django import template

register = template.Library()


def get_label(gestion):
    if gestion.tipo_gestion.code == '0002':
        return "C"
    else:
        return "S"


class puntos_Node(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<puntos Node>"

    def render(self, context):
        data = []

        for p in Paquete.objects.filter(fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year):
            if p.position:
                obj = {}
                obj['contrato'] = p.contrato
                obj['nombre'] = p.cliente
                obj['direccion'] = p.direccion
                obj['label'] = "E"
                obj['latitude'] = p.position.latitude
                obj['longitude'] = p.position.longitude
                obj['usuario'] = p.user.username
                obj['fecha'] = str(p.fecha_entrega)
                obj['resultado'] = p.tipificacion.causa
                data.append(obj)
        for g in Gestion.objects.filter(fecha_gestion__day=datetime.now().day,
            fecha_gestion__month=datetime.now().month,
            fecha_gestion__year=datetime.now().year):
            if g.position:
                obj = {}
                obj['contrato'] = g.cliente.contrato
                obj['nombre'] = g.cliente.name
                obj['direccion'] = g.cliente.direccion
                obj['label'] = get_label(g)
                obj['latitude'] = g.position.latitude
                obj['longitude'] = g.position.longitude
                obj['usuario'] = g.user.username
                obj['fecha'] = str(g.fecha_gestion)
                obj['resultado'] = g.tipo_resultado.descripcion
                data.append(obj)
        for g in Verificacion.objects.filter(
            fecha_entrega__day=datetime.now().day,
            fecha_entrega__month=datetime.now().month,
            fecha_entrega__year=datetime.now().year):
            if g.position:
                obj = {}
                obj['contrato'] = g.contrato
                obj['nombre'] = g.nombre_cliente
                obj['direccion'] = g.direccion
                obj['label'] = "V"
                obj['latitude'] = g.position.latitude
                obj['longitude'] = g.position.longitude
                obj['usuario'] = g.user.username
                obj['fecha'] = str(g.fecha_entrega)
                obj['resultado'] = g.estado
                data.append(obj)
        context[self.varname] = data
        return ''


@register.tag
def get_puntos(parser, token):
    """
        uso
            {% get_puntos as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_puntos' requiere de dos argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_puntos' requiere que el primer argumento sea 'as'")

    return puntos_Node(varname=tokens[2])

