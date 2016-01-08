import pyPdf
import os
from .models import *
import string
import random
from django.conf import settings


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


def extract_code(content):
    code = []
    todo = eliminar_letras(content).split(" ")
    for n in todo:
        if len(n) >= 10:
            code.append(n)
    return code


def comprobacion(contrato, ciclo, mes, ano):
    p = None
    queryset = Paquete.objects.filter(contrato=contrato, ciclo=ciclo, mes=mes,
        ano=ano)
    if queryset.count() > 0:
        p = queryset[0]
    if p:
        return p
    else:
        return None


def cargar_comprobante(paquete, path):
    p = Paquete.objects.get(id=paquete.id)
    p.comprobante.name = generar_ruta_comprobante(paquete, 'archivo.pdf')
    p.entrega = True
    p.save()
    ruta = os.path.join(settings.MEDIA_ROOT, get_ruta(p))
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    os.rename(path, os.path.join(settings.MEDIA_ROOT,
    p.comprobante.path))
    return p


def descomponer(path):
    data = {}
    data['carpeta'] = path.replace(os.path.basename(path), '')
    data['archivo'] = os.path.splitext(os.path.basename(path))[0][0:]
    data['extension'] = os.path.splitext(path)[1][1:]
    return data


def make_ocr(path):
    nr = os.path.join(descomponer(path)['carpeta'],
        '{}.{}'.format(descomponer(path)['archivo'] + '_ocr',
            descomponer(path)['extension']))
    os.system("pypdfocr " + path)
    os.remove(path)
    return nr


def save_content(path, content):
    f = open(os.path.join
    (descomponer(path)['carpeta'], '{}.{}'.format(
        descomponer(path)['archivo'] + '_txt', 'txt')), 'w')
    f.write(content)
    f.close()


def indexar(path, indexacion):
    pdf = None
    if indexacion.make_ocr:
        path = make_ocr(path)
    pdf = pyPdf.PdfFileReader(file(path, "r"))
    content = extract_content(pdf)
    code = extract_code(content)
    for c in code:
        p = comprobacion(c[:-6], c[-6:-4], c[-4:-2], '20' + c[-2:])
        if p:
            p.indexacion = indexacion.id
            p.exportado = False
            p.save()
            cargar_comprobante(p, path)
            return p


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


def indexar_carpeta(indexacion):
    path = indexacion.path()
    if preparar_carpeta(path):
        archivos = sorted(os.listdir(path))
        for a in archivos:
            if a[-3:] == 'pdf':
                path = os.path.join(indexacion.path(), a)
                indexar(path, indexacion)
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

