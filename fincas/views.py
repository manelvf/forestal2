# -*- coding: utf-8 -*-
import sys
import json
import csv
import time
import datetime

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from django.utils.html import escape
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.contrib.admin.views.decorators import staff_member_required

from suds import WebFault
from suds.client import Client

from fincas.models import (Finca, ViaxeCamion, Tala, 
    Deed, DeedSellers, DeedFinca,
    DateRange, DateRangeForm)
from empresas.models import Empresa


jsFiles = [settings.ADMIN_MEDIA_PREFIX + "js/jquery.min.js"]


"""
viaxes grid view
"""
@staff_member_required
def homogeneidade(request, restriction):

    empresas = Empresa.objects.all()
    empresasText = ""
    for e in empresas:
      if str(e.tipoempresa) == "Transporte":
        empresasText += str(e.pk) + ':' + e.name +";"
      
    return render(None, "homogeneidade.html",
        locals(), context_instance = RequestContext(request) )

  
"""
servizos grid view
"""
@staff_member_required
def servizogridview(request):

    return render(None, "servizogridview.html",
        locals(), context_instance = RequestContext(request) )


def assignfinca(request, id):
    viaxe = ViaxeCamion.objects.get(pk=id)

    return render(None, "assignfinca.html",
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
        try:
            s = f.dataPECLsaida.isoformat()
        except AttributeError:
            s = ""


        rows.append({"id":f.id,"cell":[f.pk,f.finca.concello.name,f.finca.poligon,f.finca.parcela,str(f.m2_permiso),p,c,e,s, f.codigoPECL, f.codigoNORFOR ]})

        
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
        print("objs.filter(" + ", ".join(query_filters) + ")")
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
      print("Unexpected error:", sys.exc_info()[0])
      return HttpResponse("FAIL")

    return HttpResponse("OK")


def listaviaxes(request, id):
    s = ""
    v = ViaxeCamion.objects.filter( origen__id = id ).order_by('dia')

    listaCamions = v

    return render(None, "homogeneidade.html",
        {"listaCamions":listaCamions, "s":s} )



def queryland(request, provincia, concello, pol, par):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPPP(provincia,concello,pol,par)
    except (WebFault, ) as e:
      return render(None, "WDSLerror.html",
          {"text":unicode(e)})
    except Exception:
      print("Unexpected error:", sys.exc_info()[0])
      raise
      
    try:
      nOfItems = int(finca.control.cudnp)
    except AttributeError:
      return render(None, "WDSLerror.html",
          {"text":u"Non se atopou a parcela"})

    if nOfItems == 1:
      refCatastral = finca.bico.bi.idbi.rc.pc1 + finca.bico.bi.idbi.rc.pc2 + finca.bico.bi.idbi.rc.car + finca.bico.bi.idbi.rc.cc1 + finca.bico.bi.idbi.rc.cc2 
    else:
      refCatastral = u""

    
    return render(None, "queryland.html",
        {"finca":finca, "refCatastral":refCatastral, "jsFiles":jsFiles, "nOfItems":nOfItems,
        "provincia":provincia, "concello":concello})



def querylandsimple(provincia, concello, pol, par):
    """
    Given data for a parcel, extracts its name and surface
    """

    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'
    try:
      client = Client(url)
      finca = client.service.Consulta_DNPPP(provincia,concello,pol,par)
    except (WebFault, ) as e:
      return render(None, "WDSLerror.html",
          {"text":unicode(e)})
    except Exception:
      print("Unexpected error:", sys.exc_info()[0])
      raise
      
    try:
      nOfItems = int(finca.control.cudnp)
    except AttributeError:
      return render(None, "WDSLerror.html",
          {"text":u"Non se atopou a parcela"})

    if nOfItems == 1:
      refCatastral = finca.bico.bi.idbi.rc.pc1 + finca.bico.bi.idbi.rc.pc2 + finca.bico.bi.idbi.rc.car + finca.bico.bi.idbi.rc.cc1 + finca.bico.bi.idbi.rc.cc2 

      try:
          return (finca.bico.bi.dt.locs.lors.lorus.npa, finca.bico.lspr.spr.dspr.ssp, refCatastral,)
      except AttributeError:
          print(dir(finca))
          return (None,None,None,)


    else:
      refCatastral = u""
      return (None,None,None,)



def querycatastral(request, provincia, concello, ref_catastral):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPRC(provincia,concello,ref_catastral)
    except (WebFault, ) as e:
      return render(None, "WDSLerror.html",
          {"text":unicode(e)})


    return render(None, "queryland.html",
        {"finca":finca, "refCatastral":ref_catastral, "jsFiles":jsFiles, "nOfItems":1,
        "provincia":provincia, "concello":concello})
    


def cell(s):
    t = u""
    for k in s:
        t += u"<td>" + unicode(k) + u"</td>"

    return t

def cleanNone(v):
    if v is None:
        return u""
    elif v == 'None':
        return u""
    else: 
        return unicode(v)

def cleanZero(v):
    if v is None:
        return 0
    elif v == 'None':
        return 0
    else:
        return v


def generateDeedCSV(request):
    """
    generates a CSV file on django folder with deed information
    """
    s = u""

    f = (u"Fincas-" + unicode(datetime.date.today()) + u"-" 
        + unicode(int(time.time())) + u".csv")

    f = "output.csv"
    writer = csv.writer(open(f, "wb"), dialect = csv.excel) 

    d = ["Nombre",
         "Ref. catastral",
         "Concello",
         "Poligono",
         "Parcela",
         "Agregado",
         "Zona",
         "ha"
        ]
    writer.writerow(d)

    ha_acum = 0
    deeds = Deed.objects.all()
    for d in deeds: 
        #s += unicode(d.date) + u"\n"
        for f in d.fincas.all():

            if d.deedType == 1:
                sellers = d.sellers.all()
                sellers = [k.name for k in sellers]
                dt = unicode("Adquirido por compraventa a " + ",".join(sellers) +
                     " en fecha " + unicode(d.date))
            else:
                dt = "Adquirido por herencia"

            l = ["poligono " + unicode(b.poligon) +
                              " parcela " + unicode(b.parcela)
                              for b in f.borders.all()
                              if b.poligon is not None]
            db = u"Limita con parcelas: " + u", ".join(l)

            s = ( 
                unicode(f.paraje_catastral),
                unicode(f.ref_catastral),
                unicode(f.concello),
                unicode(f.poligon),
                unicode(f.parcela),
                cleanZero(unicode(f.agregado)),
                cleanZero(unicode(f.zona)),
                unicode(f.ha_total),
                unicode(dt),
                unicode(db)
                )

            s = map(cleanNone, s)

            s = [t.encode("utf-8") for t in s]

            writer.writerow(s)

            ha_acum += f.ha_total
    print(d.id)
        

    s = "Total: " + str(ha_acum) + " m2"

    return HttpResponse(s)


def rewriteLandSize(request):
    """
        overwrite m2 and land size (fincas)        
    """
    fincas = Finca.objects.all()

    for f in fincas:
        datos = querylandsimple(
                f.concello.provincia.name, f.concello.name,
                f.poligon, f.parcela)

        if type(datos) != HttpResponse:
            name, surface, refCatastral = datos

            if name is not None and surface is not None:
                print(name + '-' + surface + '-' + refCatastral)
                f.paraje_catastral = name.encode('utf-8')
                f.ha_total = surface
                f.ref_catastral = refCatastral
                f.save()


    s = "OK"
    return HttpResponse(s)


@staff_member_required
def weightActions(request):
    """ shows the weight data in a date range """

    form = DateRangeForm()

    return render(None, "weightActions.html",
        locals(), context_instance = RequestContext(request) )


@staff_member_required
def weightActionsOutput(request):
    post = request.POST

    viaxes = (ViaxeCamion.objects.filter(dia__gte = post['comezo'])
    .filter(dia__lte = post['final']))

    return render(None, "weightActionsOutput.html",
        locals(), context_instance = RequestContext(request) )
