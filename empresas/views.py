# -*- coding: utf-8 -*-
import sys
import json
import os
import shutil
import datetime
import subprocess

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core import serializers

from forestal2.empresas.models import Empresa, Factura, DetalleFactura
from forestal2 import settings


def EmpresaSelect(request):
    
    empresas = Empresa.objects.all()
    r = json.dumps(empresas)

    return HttpResponse(r)


def facturagridview(request):
    return render_to_response("facturagridview.html",
        locals(), context_instance = RequestContext(request) )


def gridfactura(request):

    if request.GET.has_key("page"):
        page = int(request.GET["page"])
    else:
        page = 0
    if request.GET.has_key("rows"):
        rows = int(request.GET["rows"])
    else:
        rows = 15

    sidx = request.GET["sidx"]
    sord = request.GET["sord"]

    if sord=="desc":
      sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    """
    # is search?
    if request.GET["_search"] == "true":
        fincas = gridSearch(request, Finca, sidx)
    else:
        fincas = Finca.objects.order_by(sidx)
    """
    facturas = Factura.objects.order_by(sidx)

    total = (len(facturas)/rows) + 1

    rows = [] # result rows

    for f in facturas[start:end]:
        rows.append({"id":f.id,"cell":[f.pk,str(f.empresa),str(f.cliente),str(f.tipo),str(f.numero),str(f.emision)]})
        
    r = {
        "total":total,
        "page": page,
        "records":len(rows),
        "rows": rows
        }

    r = json.dumps(r)

    return HttpResponse(r)

def griddetallefactura(request,id):
    pass

def backup(request):
    try:
        r = subprocess.Popen(["./backup_db.sh", ], stdout=subprocess.PIPE, shell=True).communicate()[0]
    except:
        return HttpResponse(u"<b>There was an error on the backup process</b>")
        
    #r = subprocess.Popen(["./a.sh"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    return HttpResponse(str(r) + "<p>Proceso completado")


