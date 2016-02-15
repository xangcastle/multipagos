# -*- coding: utf-8 -*-
from metropolitana.models import *
from django import template

register = template.Library()


class entrega_diaria_Node(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def __repr__(self):
        return "<entrega_diaria Node>"

    def render(self, context):
            context[self.varname] = entrega_diaria.objects.all()
            return ''


@register.tag
def get_entrega_diaria(parser, token):
    """
        uso
            {% get_entrega_diaria as [varname]%}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_entrega_diaria' requiere de dos argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as':
        raise template.TemplateSyntaxError(
            "'get_entrega_diaria' requiere que el primer argumento sea 'as'")

    return entrega_diaria_Node(varname=tokens[2])

