from .models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login/')
def telecobranza(request):
    template_name = "cartera/telecobranza.html"
    if request.method == "GET":
        contrato = request.GET.get('contrato', '')
        context = RequestContext(request)
        data = {
            'resultados': TipoResultado.objects.all().order_by('descripcion'),
            'cliente': Cliente.objects.get(contrato=contrato)
            }
    if request.method == "POST":
        pass

    return render_to_response(template_name, data, context_instance=context)

