# -*- coding: utf-8 -*-
import sys
import json
import csv
import time
import datetime

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.shortcuts import render
from django.urls import resolve
from django.conf import settings
from django.core import serializers
from django.utils.html import escape
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.contrib.admin.views.decorators import staff_member_required

# from suds import WebFault  # Commented out - will install later
# from suds.client import Client  # Commented out - will install later

from fincas.models import (Finca, ViaxeCamion, Tala, 
    Deed, DeedSellers, DeedFinca,
    DateRange, DateRangeForm)
from empresas.models import Empresa


jsFiles = [settings.STATIC_URL + "admin/js/jquery.min.js"]


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
      
    return render(request, "homogeneidade.html",
        locals())

  
"""
servizos grid view
"""
@staff_member_required
def servizogridview(request):

    return render(request, "servizogridview.html",
        locals())


@staff_member_required
def assignfinca(request, id):
    from django.shortcuts import get_object_or_404
    viaxe = get_object_or_404(ViaxeCamion, pk=id)

    return render(request, "assignfinca.html",
        {"viaxe": viaxe})


"""
Grid de servizos forestais
"""

@staff_member_required
def grid(request):
    try:
        page = int(request.GET.get("page", 1))
        rows = int(request.GET.get("rows", 15))
        sidx = request.GET.get("sidx", "id")
        sord = request.GET.get("sord", "asc")

        # Validate bounds
        if page < 1:
            page = 1
        if rows < 1 or rows > 1000:
            rows = 15

        # Map frontend field names to database fields
        field_mapping = {
            'concello': 'finca__concello',
            'poligono': 'finca__poligon',
            'parcela': 'finca__parcela'
        }
        sidx = field_mapping.get(sidx, sidx)

        # Validate sort field
        if '__' not in sidx:
            valid_fields = [f.name for f in Tala._meta.get_fields()]
            if sidx not in valid_fields:
                sidx = "id"

        # Validate sort order
        if sord not in ["asc", "desc"]:
            sord = "asc"

    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    if sord == "desc":
        sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    if request.GET.get("_search") == "true":
        talas = gridSearch(request, Tala, sidx)
    else:
        # Optimize with select_related to avoid N+1 queries
        talas = Tala.objects.select_related('finca__concello').order_by(sidx)

    total = (len(talas)//rows) + 1

    result_rows = [] # result rows

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


        result_rows.append({"id":f.id,"cell":[f.pk,f.finca.concello.name,f.finca.poligon,f.finca.parcela,str(f.m2_permiso),p,c,e,s, f.codigoPECL, f.codigoNORFOR ]})

    r = {
        "total": total,
        "page": page,
        "records": len(result_rows),
        "rows": result_rows
    }

    return JsonResponse(r)


"""
Grid de fincas
"""

@staff_member_required
def gridfinca(request):
    try:
        page = int(request.GET.get("page", 1))
        rows = int(request.GET.get("rows", 15))
        sidx = request.GET.get("sidx", "id")
        sord = request.GET.get("sord", "asc")

        # Validate bounds
        if page < 1:
            page = 1
        if rows < 1 or rows > 1000:
            rows = 15

        # Validate sort field
        valid_fields = [f.name for f in Finca._meta.get_fields()]
        if sidx not in valid_fields:
            sidx = "id"

        # Validate sort order
        if sord not in ["asc", "desc"]:
            sord = "asc"

    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    if sord == "desc":
        sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    # is search?
    if request.GET.get("_search") == "true":
        fincas = gridSearch(request, Finca, sidx)
    else:
        # Optimize with select_related
        fincas = Finca.objects.select_related('concello', 'dono').order_by(sidx)

    total = (len(fincas)//rows) + 1

    result_rows = [] # result rows

    for f in fincas[start:end]:
        result_rows.append({"id":f.id,"cell":[f.pk,f.concello.name,f.zona,f.poligon,f.parcela,f.ha_total,str(f.dono)]})

    r = {
        "total": total,
        "page": page,
        "records": len(result_rows),
        "rows": result_rows
    }

    return JsonResponse(r)


"""
Shows viaxes without origin or destination or all
"""
@staff_member_required
def gridviaxe(request, servizo=None):
    try:
        page = int(request.GET.get("page", 1))
        rows = int(request.GET.get("rows", 15))
        sidx = request.GET.get("sidx", "id")
        sord = request.GET.get("sord", "asc")
        restriction = request.GET.get("restriction", "")

        # Validate bounds
        if page < 1:
            page = 1
        if rows < 1 or rows > 1000:
            rows = 15

        # Validate sort field
        valid_fields = [f.name for f in ViaxeCamion._meta.get_fields()]
        if sidx not in valid_fields:
            sidx = "id"

        # Validate sort order
        if sord not in ["asc", "desc"]:
            sord = "asc"

    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    if sord == "desc":
        sidx = "-" + sidx

    start = (page-1)*rows
    end = (page)*rows

    if servizo is not None:
        viaxes = ViaxeCamion.objects.filter(origen__pk=servizo)
    elif request.GET.get("_search") == "true":
        viaxes = gridSearch(request, ViaxeCamion)
    elif restriction == "origin":
        viaxes = ViaxeCamion.objects.filter(Q(origen__isnull=True) | Q(origen__exact=''))
    elif restriction == "destination":
        viaxes = ViaxeCamion.objects.filter(Q(destino__isnull=True) | Q(destino__exact=''))
    else:
        viaxes = ViaxeCamion.objects.all()

    # Fix N+1 query problem with prefetch_related
    viaxes = viaxes.prefetch_related('origen__finca__concello', 'camion', 'destino').order_by(sidx)

    total = (len(viaxes)//rows) + 1

    result_rows = []
    for v in viaxes[start:end]:
        s = ""
        last_origin_pk = 0
        # No additional queries here thanks to prefetch_related
        for o in v.origen.all():
            s += str(o.finca.concello.name) + ": " + str(o.finca.poligon) + "-" + str(o.finca.parcela)
            last_origin_pk = o.pk

        if len(v.obs) > 0:
            obs = "S"
        else:
            obs = ""
        result_rows.append({"id":v.id,"cell":[v.pk, str(v.dia), str(v.camion), v.tm, s, str(v.destino), v.n_talonario, obs, last_origin_pk]})

    r = {
        "total": total,
        "page": page,
        "records": len(viaxes),
        "rows": result_rows
    }

    return JsonResponse(r)


"""
  Grid WebServices
"""

def gridservizo(request):
    pass

def gridSearch(request, model, sidx=None):
    import logging
    logger = logging.getLogger(__name__)

    filters = json.loads(request.GET["filters"])

    # Whitelist of allowed operations
    ALLOWED_OPS = {
        'eq': '',
        'ne': 'ne',
        'lt': 'lt',
        'le': 'lte',
        'gt': 'gt',
        'ge': 'gte',
        'bw': 'startswith',  # begins with
        'bn': 'startswith',   # doesn't begin with (negated)
        'ew': 'endswith',     # ends with
        'en': 'endswith',     # doesn't end with (negated)
        'cn': 'contains',     # contains
        'nc': 'contains',     # doesn't contain (negated)
    }

    # Get valid fields for the model
    valid_fields = {f.name for f in model._meta.get_fields()}

    rules = []
    if model == Tala:
        for f in filters["rules"]:
            field = f["field"]
            # Check if field exists in Tala model
            if field not in valid_fields:
                # Try with finca__ prefix
                field = "finca__" + field
            f["field"] = field
            rules.append(f)
    else:
        rules = filters["rules"]

    # Build Q objects safely
    query = Q()
    for r in rules:
        field = r.get("field", "")
        op = r.get("op", "eq")
        data = r.get("data", "")

        # Validate operation
        if op not in ALLOWED_OPS:
            logger.warning(f"Invalid operation: {op}")
            continue

        # Validate field name - only allow alphanumeric and underscores
        if not all(c.isalnum() or c == '_' for c in field.replace('__', '')):
            logger.warning(f"Invalid field name: {field}")
            continue

        # Build the filter lookup
        lookup_op = ALLOWED_OPS[op]
        if lookup_op:
            lookup = f"{field}__{lookup_op}"
        else:
            lookup = field

        # Build Q object
        try:
            q_obj = Q(**{lookup: data})

            # Combine with existing query
            if filters.get("groupOp") == "OR":
                query |= q_obj
            else:
                query &= q_obj
        except Exception as e:
            logger.error(f"Error building query for {field}: {e}")
            continue

    # Apply the query filter
    objs = model.objects.filter(query) if query else model.objects.all()

    if sidx:
        objs = objs.order_by(sidx)

    return objs


from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

@staff_member_required
@require_http_methods(["POST"])
def assocfincaservizo(request):
    try:
        finca = request.POST.get("finca")
        servizo = request.POST.get("servizo")

        if not finca or not servizo:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        from django.shortcuts import get_object_or_404
        finca_obj = get_object_or_404(Finca, pk=finca)
        updated = Tala.objects.filter(pk=servizo).update(finca=finca)

        if updated:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Servizo not found'}, status=404)

    except Exception as e:
        logger.exception(f"Error in assocfincaservizo: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)


from django.db import transaction

@staff_member_required
@require_http_methods(["POST"])
@transaction.atomic
def assocservizoviaxe(request):
    try:
        servizo = request.POST.get("servizo")
        viaxe = request.POST.get("viaxe")

        if not servizo or not viaxe:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        from django.shortcuts import get_object_or_404
        vc = get_object_or_404(ViaxeCamion, pk=viaxe)

        # Atomic operation - clear and add
        vc.origen.clear()
        vc.origen.add(servizo)

        return JsonResponse({'success': True})

    except Exception as e:
        logger.exception(f"Error in assocservizoviaxe: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)


@staff_member_required
@require_http_methods(["POST"])
@transaction.atomic
def desassocviaxeservizo(request):
    try:
        servizo = request.POST.get("servizo")
        viaxe = request.POST.get("viaxe")

        if not viaxe:
            return JsonResponse({'error': 'Missing viaxe parameter'}, status=400)

        from django.shortcuts import get_object_or_404
        vc = get_object_or_404(ViaxeCamion, pk=viaxe)

        # Clear all origins atomically
        vc.origen.clear()

        return JsonResponse({'success': True})

    except Exception as e:
        logger.exception(f"Error in desassocviaxeservizo: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)


@staff_member_required
@require_http_methods(["POST"])
@transaction.atomic
def joinviaxefinca(request):
    try:
        idviaxe = request.POST.get("idviaxe")
        idtala = request.POST.get("idtala")
        action = request.POST.get("action")

        if not idviaxe or not idtala or not action:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        from django.shortcuts import get_object_or_404
        viaxe = get_object_or_404(ViaxeCamion, pk=idviaxe)
        tala = get_object_or_404(Tala, pk=idtala)

        if action == "ligar":
            viaxe.origen.add(tala)
        else:
            viaxe.origen.clear()

        return JsonResponse({'success': True})

    except ViaxeCamion.DoesNotExist:
        return JsonResponse({'error': 'Viaxe not found'}, status=404)
    except Tala.DoesNotExist:
        return JsonResponse({'error': 'Tala not found'}, status=404)
    except Exception as e:
        logger.exception(f"Error in joinviaxefinca: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)


@staff_member_required
def listaviaxes(request, id):
    # Fix N+1 query problem with prefetch_related
    v = ViaxeCamion.objects.filter(origen__id=id).select_related('camion', 'destino').order_by('dia')

    return render(request, "homogeneidade.html",
        {"listaCamions": v})



@staff_member_required
def queryland(request, provincia, concello, pol, par):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPPP(provincia, concello, pol, par)
    except WebFault as e:
      logger.error(f"WebFault in queryland: {e}")
      return render(request, "WDSLerror.html",
          {"text": str(e)})
    except Exception as e:
      logger.exception(f"Unexpected error in queryland: {e}")
      raise
      
    try:
      nOfItems = int(finca.control.cudnp)
    except AttributeError:
      return render(request, "WDSLerror.html",
          {"text":"Non se atopou a parcela"})

    if nOfItems == 1:
      refCatastral = finca.bico.bi.idbi.rc.pc1 + finca.bico.bi.idbi.rc.pc2 + finca.bico.bi.idbi.rc.car + finca.bico.bi.idbi.rc.cc1 + finca.bico.bi.idbi.rc.cc2 
    else:
      refCatastral = ""

    
    return render(request, "queryland.html",
        {"finca":finca, "refCatastral":refCatastral, "jsFiles":jsFiles, "nOfItems":nOfItems,
        "provincia":provincia, "concello":concello})



def querylandsimple(provincia, concello, pol, par):
    """
    Given data for a parcel, extracts its name and surface
    """

    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'
    try:
      client = Client(url)
      finca = client.service.Consulta_DNPPP(provincia, concello, pol, par)
    except WebFault as e:
      logger.error(f"WebFault in querylandsimple: {e}")
      return render(request, "WDSLerror.html",
          {"text": str(e)})
    except Exception as e:
      logger.exception(f"Unexpected error in querylandsimple: {e}")
      raise
      
    try:
      nOfItems = int(finca.control.cudnp)
    except AttributeError:
      return render(request, "WDSLerror.html",
          {"text":"Non se atopou a parcela"})

    if nOfItems == 1:
      refCatastral = finca.bico.bi.idbi.rc.pc1 + finca.bico.bi.idbi.rc.pc2 + finca.bico.bi.idbi.rc.car + finca.bico.bi.idbi.rc.cc1 + finca.bico.bi.idbi.rc.cc2 

      try:
          return (finca.bico.bi.dt.locs.lors.lorus.npa, finca.bico.lspr.spr.dspr.ssp, refCatastral,)
      except AttributeError as e:
          logger.warning(f"AttributeError in querylandsimple: {e}")
          return (None, None, None,)


    else:
      refCatastral = ""
      return (None,None,None,)



@staff_member_required
def querycatastral(request, provincia, concello, ref_catastral):
    url = 'https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx?WSDL'

    try:
      client = Client(url)
      finca = client.service.Consulta_DNPRC(provincia, concello, ref_catastral)
    except WebFault as e:
      logger.error(f"WebFault in querycatastral: {e}")
      return render(request, "WDSLerror.html",
          {"text": str(e)})


    return render(request, "queryland.html",
        {"finca":finca, "refCatastral":ref_catastral, "jsFiles":jsFiles, "nOfItems":1,
        "provincia":provincia, "concello":concello})
    


def cell(s):
    t = ""
    for k in s:
        t += "<td>" + str(k) + "</td>"

    return t

def cleanNone(v):
    if v is None:
        return ""
    elif v == 'None':
        return ""
    else: 
        return str(v)

def cleanZero(v):
    if v is None:
        return 0
    elif v == 'None':
        return 0
    else:
        return v


@staff_member_required
def generateDeedCSV(request):
    """
    generates a CSV file with deed information and returns it for download
    """
    import io

    filename = f"Fincas-{datetime.date.today()}-{int(time.time())}.csv"

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output, dialect=csv.excel)

    # Write header
    header = ["Nombre", "Ref. catastral", "Concello", "Poligono", "Parcela",
              "Agregado", "Zona", "ha", "Tipo", "Limites"]
    writer.writerow(header)

    ha_acum = 0
    # Optimize query with prefetch_related
    deeds = Deed.objects.prefetch_related('sellers', 'fincas__borders').all()

    for deed in deeds:
        for finca in deed.fincas.all():
            if deed.deedType == 1:
                sellers = [k.name for k in deed.sellers.all()]
                dt = f"Adquirido por compraventa a {', '.join(sellers)} en fecha {deed.date}"
            else:
                dt = "Adquirido por herencia"

            borders = [f"poligono {b.poligon} parcela {b.parcela}"
                      for b in finca.borders.all()
                      if b.poligon is not None]
            db = "Limita con parcelas: " + ", ".join(borders) if borders else ""

            row = [
                cleanNone(finca.paraje_catastral),
                cleanNone(finca.ref_catastral),
                cleanNone(str(finca.concello)),
                cleanNone(str(finca.poligon)),
                cleanNone(str(finca.parcela)),
                cleanZero(finca.agregado),
                cleanZero(finca.zona),
                cleanNone(str(finca.ha_total)),
                dt,
                db
            ]

            writer.writerow(row)
            ha_acum += finca.ha_total or 0

    logger.info(f"Generated CSV with {ha_acum} total ha")

    # Create HTTP response
    response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@staff_member_required
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

    return render(request, "weightActions.html",
        locals())


@staff_member_required
def weightActionsOutput(request):
    post = request.POST

    viaxes = (ViaxeCamion.objects.filter(dia__gte = post['comezo'])
    .filter(dia__lte = post['final']))

    return render(request, "weightActionsOutput.html",
        locals())
