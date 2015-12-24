# -*- coding: utf-8 -*-
import pyPdf
import os
from .models import *
from metropolitana.models import Paquete
import string
import random
from django.conf import settings
import math


def generar_paginas(paquetes, by_page=6.0):
    paginas = []
    numero = 1
    comprobantes = paquetes.order_by('orden_impresion')
    if comprobantes:
        pagina = {'comprobantes': []}
        pagina['numero'] = numero
        total_paginas = int(math.ceil(comprobantes.count() / by_page))
        for p in range(0, total_paginas):
            for i in range(p, int(total_paginas * int(by_page)), total_paginas):
                try:
                    pagina['comprobantes'].append(comprobantes[i])
                except:
                    pagina['comprobantes'].append(Paquete())
                if len(pagina['comprobantes']) == int(by_page):
                    numero += 1
                    paginas.append(pagina)
                    pagina = {'comprobantes': []}
                    pagina['numero'] = numero
    return paginas


def get_media_url(model, filename):
    clase = model.__class__.__name__
    code = str(model.id)
    return '%s/%s/%s' % (clase, code, filename)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def limpiar_caracteres(texto):
    for l in texto:
        if l not in ['A', 'B', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J''K', 'L',
            'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            ' ']:
            texto = texto.replace(l, '')
    return texto


def limpiar_espacios(texto):
    texto = texto.replace(' ', '')
    return texto


def eliminar_letras(texto):
    for l in texto:
        if l not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']:
            texto = texto.replace(l, '')
    return texto


def extract_content(pdf):
    content = ""
    content += pdf.getPage(0).extractText() + "\n"
    content = content.encode("ascii", "ignore")
    content = " ".join(content.replace("\xa0", " ").strip().split())
    return content


def extract_cedula(content, option):
    code = ''
    if option == 1:
        i = content.find("IDENTIFICACION #") + 16
        f = i + 14
        code = limpiar_espacios(content[i:f])
        #print code
    if option == 2:
        i = content.find("CODE") + 4
        f = i + 15
        code = limpiar_espacios(eliminar_letras(content[i:f]))
        #print code
    if option == 3:
        f = content.find("#") - 5
        i = f - 16
        code = limpiar_espacios(eliminar_letras(content[i:f]))
        #print code
    if option == 4:
        todo = eliminar_letras(content).split(" ")
        for n in todo:
            if len(n) >= 10:
                code = n
        #print code
    if option == 5:
        f = content.find("LOTE")
        i = f - 13
        code = limpiar_espacios(eliminar_letras(content[i:f]))
        #print code
    if not len(code) >= 10:
        code = '0000000000'
    return code


def comprobacion(cedula):
    p = None
    queryset = Empleado.objects.filter(cedula=cedula)
    if queryset.count() > 0:
        p = queryset[0]
    if p:
        print p.nombre
        return p
    else:
        return None


def cargar_ecuenta(empleado, path):
    empleado.ecuenta.name = get_media_url(empleado, 'archivo.pdf')
    empleado.save()
    ruta = empleado.ecuenta.path
    carpeta = ruta.replace(os.path.basename(ruta), '')
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    os.rename(path, os.path.join(settings.MEDIA_ROOT,
    empleado.ecuenta.path))


def carga_manual(path, fecha):
    ruta = "/home/abel/indexacion/" + str(fecha)
    archivo = os.path.splitext(os.path.basename(path))[0][0:]
    extension = os.path.splitext(path)[1][1:]
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    os.rename(path, os.path.join(ruta, '{}.{}'.format(archivo, extension)))


def indexar(path, fecha=None):
    carpeta = path.replace(os.path.basename(path), '')
    archivo = os.path.splitext(os.path.basename(path))[0][0:]
    #extension = os.path.splitext(path)[1][1:]
    #nr = os.path.join(carpeta, '{}.{}'.format(archivo + '_ocr', extension))
    #os.system("pypdfocr " + path)
    pdf = pyPdf.PdfFileReader(file(path, "r"))
    content = extract_content(pdf)
    f = open(os.path.join
    (carpeta, '{}.{}'.format(archivo + '_txt', 'txt')), 'w')
    f.write(content)
    f.close()
    cedula = extract_cedula(content, 1)
    print cedula
    p = comprobacion(cedula)
    if p:
        cargar_ecuenta(p, path)
    else:
        carga_manual(path, fecha)
    #os.remove(nr)


def preparar_carpeta(path):
    comand = "cd %s && mkdir tm && pdftk *.pdf cat output tm/1.pdf && rm *.pdf"
    comand += " && mv tm/1.pdf 1.pdf && pdftk 1.pdf burst"
    comand += " && rm doc_data.txt 1.pdf && rm -rf tm"
    comand = comand % (path)
    try:
        os.system(comand)
        return True
    except:
        return False


def indexar_carpeta(path, fecha):
    if preparar_carpeta(path):
        archivos = sorted(os.listdir(path))
        for a in archivos:
            if a[-3:] == 'pdf':
                indexar(os.path.join(path, a), fecha)
        #os.system("rm -rf %s" % path)


def recoger_archivos(fecha):
    o = '/home/abel/workspace/deltacopiers/deltacopiers/media'
    d = o + '/TEMP/' + id_generator()
    comand = "mkdir %s && mv %s/*.pdf %s" % (d, o, d)
    try:
        os.system(comand)
    except:
        pass
    indexar_carpeta(d, fecha)


if __name__ == "__main__":
    import sys
    indexar_carpeta(sys.argv[1])



