# -*- coding: utf-8 -*-


def verificar_estado(verificaciones):
    for v in verificaciones:
        v.estado = v.get_estado()
        v.save()