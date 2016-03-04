# -*- coding: utf-8 -*-
from metropolitana.models import Zona
from django import template

register = template.Library()


class barrios_Node(template.Node):
    def __init__(self, varname1, varname2):
        self.varname1 = varname1
        self.varname2 = varname2

    def __repr__(self):
        return "<barrios Node>"

    def render(self, context):
        context[self.varname1] = Zona.objects.get(id=int(self.varname2)
        ).barrios()
        return ''


@register.tag
def get_barrios(parser, token):
    """uso{% get_puntos as [varname] where_zona_is [varname] %}
    """
    tokens = token.contents.split()
    args = len(tokens)

    if not len(tokens) == 3:
        raise template.TemplateSyntaxError(
            "'get_barrios' requiere de cinco argumentos y se dieron %s"
            % (args))
    if not tokens[1] == 'as' and not tokens[3] == 'where_zona_is':
        raise template.TemplateSyntaxError(
            """'get_puntos' requiere que el primer argumento sea 'as'
            y que el tecero sea 'where_zona_is'""")

    return barrios_Node(varname1=tokens[2], varname2=tokens[4])

