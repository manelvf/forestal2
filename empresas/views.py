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
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core import serializers, urlresolvers

from forestal2.empresas.models import Empresa, Factura, DetalleFactura
from forestal2.fincas.models import Tala
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
    detallefacturas = DetalleFactura.objects.filter(factura=id).order_by(sidx)

    total = (len(detallefacturas)/rows) + 1

    rows = [] # result rows

    for f in detallefacturas[start:end]:
        rows.append({"id":f.id,"cell":[f.pk,str(f.servizo),str(f.concepto),str(f.tipo_iva),str(f.tipo_irpf),str(f.cantidad),str(f.valor)]})
        
    r = {
        "total":total,
        "page": page,
        "records":len(rows),
        "rows": rows
        }

    r = json.dumps(r)

    return HttpResponse(r)


"""
  Never use empty 'factura' id
"""
def adddetallefactura(request, id=None):
    if id is None:
        return HttpResponse("Detalle Factura mush have a factura id")

    factura = Factura.objects.get(pk=id)
    df = DetalleFactura(factura=factura)
    df.save()
    return HttpResponse("OK")
    #return redirect(urlresolvers.reverse('admin:empresas_detallefactura_change', args=(df.id,)))


"""
  Servizo forestal to Detalle Factura association
"""
def assocservizodetalle(request):
    detalle = request.GET["detalle"]
    servizo = request.GET["servizo"]

    servizoObj = Tala.objects.get(pk=servizo)
    DetalleFactura.objects.filter(pk=detalle).update(servizo=servizoObj)

    return HttpResponse("OK")


"""
  Related functions
"""

def backup(request):
    try:
        r = subprocess.Popen(["./backup_db.sh", ], stdout=subprocess.PIPE, shell=True).communicate()[0]
    except:
        return HttpResponse(u"<b>There was an error on the backup process</b>")
        
    #r = subprocess.Popen(["./a.sh"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    return HttpResponse(str(r) + "<p>Proceso completado")


"""
  Spreadsheet export
"""
def exportgrid(request):
    print str(request.POST)
    return HttpResponse("")

