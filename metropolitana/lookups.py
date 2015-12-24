# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.html import escape
from ajax_select import LookupChannel
from .models import *


class PaqueteLookup(LookupChannel):

    model = Paquete

    def get_query(self, q, request):
        return Paquete.objects.filter(
            Q(cliente__icontains=q) |
            Q(barra__icontains=q) |
            Q(factura=q))

    def get_result(self, obj):
        return obj.factura

    def format_match(self, obj):
        #return '%s<div><i>%s</i></div><div><i>%s</i></div>' \
        #% (escape(obj.cliente), escape(obj.factura), escape(obj.departamento),
           #escape(obj.municipio), escape(obj.barrio), escape(obj.lote))
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return '<div>cliente : %s</div><div> departamento : %s</div><div> municipio : %s</div><div> lote : %s</div>' \
        % (escape(obj.cliente), escape(obj.departamento),
            escape(obj.municipio), escape(obj.lote.numero))
