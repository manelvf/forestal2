# -*- coding: utf-8 -*-
import sys
import json

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.conf import settings
from django.core import serializers
from django.utils.html import escape

from suds import WebFault
from suds.client import Client

from forestal2.fincas.models import Finca, ViaxeCamion, Tala
from forestal2.empresas.models import Empresa


jsFiles = [settings.ADMIN_MEDIA_PREFIX + "js/jquery.min.js"]


"""
viaxes grid view
"""
def homogeneidade(request, restriction):

    empresas = Empresa.objects.all()
    empresasText = ""
    for e in empresas:
      if str(e.tipoempresa) == "Transporte":
        empresasText += str(e.pk) + ':' + e.name +";"
      
      

    return render_to_response("homogeneidade.html",
        locals(), context_instance = RequestContext(request) )

  
"""
servizos grid view
"""
def servizogridview(request):

    return render_to_response("servizogridview.html",
        locals(), context_instance = RequestContext(request) )


def assignfinca(request, id):
    viaxe = ViaxeCamion.objects.get(pk=id)

    return render_to_response("assignfinca.html",
        locals(), context_instance = RequestContext(request) )


"""
Grid de servizos forestais
"""

def grid(request):
    
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

    if sidx == 'concello' : sidx = 'finca__concello'
    elif sidx == 'poligono' : sidx = 'finca__poligon'
    elif sidx == 'parcela' : sidx = 'finca__parcela'

    if sord=="desc":
      sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    if request.GET["_search"] == "true":
        talas = gridSearch(request,Tala,sidx)
    else:
        talas = Tala.objects.order_by(sidx)

    total = (len(talas)/rows) + 1

    rows = [] # result rows

    """
    Assign permiso, comezo, entradaGrupo
    """
    for f in talas[start:end]:
        try:
            p = f.permiso.isoformat()
        except AttributeError:
            p = ""
        try:
            c = f.comezo.isoformat()
        except AttributeError:
            c = ""
        try:
            e = f.entradaGrupo.isoformat()
        except AttributeError:
            e = ""


        rows.append({"id":f.id,"cell":[f.pk,f.finca.concello.name,f.finca.poligon,f.finca.parcela,p,c,e, f.codigoPECL, f.codigoNORFOR ]})

        
    r = {
        "total":total,
        "page": page,
        "records":len(rows),
        "rows": rows
        }

    r = json.dumps(r)

    return HttpResponse(r)


"""
Grid de fincas
"""

def gridfinca(request):
    
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

    # is search?
    if request.GET["_search"] == "true":
        fincas = gridSearch(request, Finca, sidx)
    else:
        fincas = Finca.objects.order_by(sidx)

    total = (len(fincas)/rows) + 1

    rows = [] # result rows

    for f in fincas[start:end]:
        rows.append({"id":f.id,"cell":[f.pk,f.concello.name,f.zona,f.poligon,f.parcela,f.ha_total,str(f.dono)]})
        
    r = {
        "total":total,
        "page": page,
        "records":len(rows),
        "rows": rows
        }

    r = json.dumps(r)

    return HttpResponse(r)


"""
Shows viaxes without origin or destination or all
"""
def gridviaxe(request, servizo=None):

    page = int(request.GET["page"])
    rows = int(request.GET["rows"])

    sidx = request.GET["sidx"]
    sord = request.GET["sord"]

    restriction = request.GET["restriction"]

    if sord=="desc":
      sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    if servizo is not None:
        viaxes = ViaxeCamion.objects.filter(origen__pk = servizo) 
    elif request.GET["_search"] == "true":     # is search?
        viaxes = gridSearch(request, ViaxeCamion)
    elif restriction == "origin":
      viaxes = ViaxeCamion.objects.filter( Q(origen__isnull=True) 
        or Q(origen__isblank=True)
        )
    elif restriction == "destination":
      viaxes = ViaxeCamion.objects.filter( Q(destino__isnull=True) 
        or Q(destino__isblank=True))
    else:
      viaxes = ViaxeCamion.objects.all()

    viaxes = viaxes.order_by(sidx)

    total = (len(viaxes)/rows) + 1

    rows = []
    for v in viaxes[start:end]:
        s = u""
        last_origin_pk = 0
        for o in v.origen.all():
            s += unicode(o.finca.concello.name) + u": " + unicode(o.finca.poligon) + u"-" + unicode(o.finca.parcela)
            last_origin_pk = o.pk

        if len(v.obs) > 0:
            obs = "S"
        else:
            obs = ""
        rows.append({"id":v.id,"cell":[v.pk, unicode(v.dia), unicode(v.camion), v.tm, s, unicode(v.destino), v.n_talonario, obs, last_origin_pk]})


    r = {
        "total":total,
        "page": page,
        "records":len(viaxes),
        "rows": rows
        }

    r = json.dumps(r)
    return HttpResponse(r)


"""
  Grid WebServices
"""

def gridservizo(request):
    pass

def gridSearch(request, model, sidx=None): 

    filters = json.loads(request.GET["filters"])

    rules = []
    if model==Tala:
        for f in filters["rules"]:
            try:
                Tala._meta.get_field_by_name(f["field"])
            except:
                f["field"] = "finca__"+f["field"]
            rules.append(f)
    else:
        rules = filters["rules"]


    query_filters = []
    for r in rules:
        try:
            d = float(r["data"])
            d = unicode(d)
        except ValueError:
            d = "'" + escape(r["data"]) + "'" 

        if r["op"] == "eq":
            query_filters.append('Q(' + r["field"] + u"=" + d + ')')
        else :
            query_filters.append('Q(' + r["field"] + u"__" + r["op"] + u"=" + d + ')')

    objs = model.objects.all()


    if filters["groupOp"] == "OR":
        objs = eval("objs.filter(" + " | ".join(query_filters) + ")")
    else:
        print "objs.filter(" + ", ".join(query_filters) + ")"
        objs = eval("objs.filter(" + ", ".join(query_filters) + ")")

    if sidx:
        objs = objs.order_by(sidx)
    
    return objs


def assocfincaservizo(request):
    finca = request.GET["finca"]
    servizo = request.GET["servizo"]

    finca_obj = Finca.objects.get(pk=finca)
    Tala.objects.filter(pk=servizo).update(finca = finca)


    return HttpResponse("OK")


def assocservizoviaxe(request):
    servizo = request.GET["servizo"]
    viaxe = request.GET["viaxe"]

    vc = ViaxeCamion.objects.get(pk=viaxe)
    for v in vc.origen.all():
        vc.origen.remove(v)

    vc.origen.add(servizo)


    return HttpResponse("OK")


def desassocviaxeservizo(request):
    servizo = request.GET["servizo"]
    viaxe = request.GET["viaxe"]

    vc = ViaxeCamion.objects.get(pk=viaxe)
    for v in vc.origen.all():
        vc.origen.remove(v)


    return HttpResponse("OK")


def joinviaxefinca(request):
    idviaxe = request.GET["idviaxe"]
    idtala= request.GET["idtala"]
    action = request.GET["action"]

    return HttpResponse("OK")
    try:
      viaxe = ViaxeCamion.objects.get(pk=idviaxe)
      tala = Tala.objects.get(pk=idtala)

      if action=="ligar":
        viaxe.origen.add(tala)
      else:
        viaxe.origen.clear()

    except:
      print "Unexpected error:", sys.exc_info()[0]
      return HttpResponse("FAIL")

    return HttpResponse("OK")


def listaviaxes(request, id):
    s = ""
    v = ViaxeCamion.objects.filter( origen__id = id ).order_by('dia')

    listaCamions = v

    return render_to_response("homogeneidade.html",
        {"listaCamions":listaCamions, "s":s} )



def queryland(request, provincia, concello, pol, par):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPPP(provincia,concello,pol,par)
    except WebFault,e:
      return render_to_response("WDSLerror.html",
          {"text":unicode(e)})
    except Exception:
      print "Unexpected error:", sys.exc_info()[0]
      raise
      
    try:
      nOfItems = int(finca.control.cudnp)
    except AttributeError:
      return render_to_response("WDSLerror.html",
          {"text":u"Non se atopou a parcela"})

    if nOfItems == 1:
      refCatastral = finca.bico.bi.idbi.rc.pc1 + finca.bico.bi.idbi.rc.pc2 + finca.bico.bi.idbi.rc.car + finca.bico.bi.idbi.rc.cc1 + finca.bico.bi.idbi.rc.cc2 
    else:
      refCatastral = u""

    
    return render_to_response("queryland.html",
        {"finca":finca, "refCatastral":refCatastral, "jsFiles":jsFiles, "nOfItems":nOfItems,
        "provincia":provincia, "concello":concello})

def querycatastral(request, provincia, concello, ref_catastral):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPRC(provincia,concello,ref_catastral)
    except WebFault,e:
      return render_to_response("WDSLerror.html",
          {"text":unicode(e)})


    return render_to_response("queryland.html",
        {"finca":finca, "refCatastral":ref_catastral, "jsFiles":jsFiles, "nOfItems":1,
        "provincia":provincia, "concello":concello})
    
