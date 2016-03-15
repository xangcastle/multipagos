# -*- coding: utf-8 -*-
from metropolitana.models import *
from django import template

register = template.Library()


class barriosH_Node(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<Get Barrios Node>"

    def render(self, context):
            context[self.varname] = Barrio.objects.all().exclude(id__in=
            zona_barrio.objects.all().values_list('barrio', flat=True))
            return ''


@register.tag
def get_barrios_huerfanos(parser, token):
    """
        uso
            {% get_barrios_huerfanos as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_barrios_huerfanos' requiere de dos argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_barrios_huerfanos' requiere que el primer argumento sea 'as'")

    return barriosH_Node(varname=tokens[2])

