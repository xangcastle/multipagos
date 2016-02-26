# -*- coding: utf-8 -*-
from metropolitana.models import *
from datetime import datetime
from django import template

register = template.Library()


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
                data.append(p)
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

