# -*- coding: utf-8 -*-
from metropolitana.models import *
from django import template

register = template.Library()


class estadisticas_all_Node(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<GetEstadisticas Node>"

    def render(self, context):
            context[self.varname] = EstadisticaCiclo.objects.all(
                ).order_by('-ano', '-mes', 'ciclo')[:12]
            return ''


@register.tag
def get_estadisticas_all(parser, token):
    """
        uso
            {% get_estadisticas_all as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_estadisticas' requiere de dos argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_estadisticas_all' requiere que el primer argumento sea 'as'")

    return estadisticas_all_Node(varname=tokens[2])

