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
from django.shortcuts import render, redirect
from django.urls import resolve
from django.conf import settings
from django.core import serializers

from empresas.models import Empresa, Factura, DetalleFactura
from fincas.models import Tala
from django.conf import settings


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def EmpresaSelect(request):
    empresas = list(Empresa.objects.all().values('id', 'name', 'nif', 'tipoempresa__name'))
    return JsonResponse(empresas, safe=False)


@staff_member_required
def facturagridview(request):
    return render(request, "facturagridview.html", {})


@staff_member_required
def gridfactura(request):
    import logging
    logger = logging.getLogger(__name__)

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
        valid_fields = [f.name for f in Factura._meta.get_fields()]
        if sidx not in valid_fields:
            sidx = "id"

        # Validate sort order
        if sord not in ["asc", "desc"]:
            sord = "asc"
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

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

    total = (len(facturas)//rows) + 1

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


@staff_member_required
def griddetallefactura(request, id):
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
        valid_fields = [f.name for f in DetalleFactura._meta.get_fields()]
        if sidx not in valid_fields:
            sidx = "id"

        # Validate sort order
        if sord not in ["asc", "desc"]:
            sord = "asc"
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

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

    total = (len(detallefacturas)//rows) + 1

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
@staff_member_required
def adddetallefactura(request, id=None):
    if id is None:
        return JsonResponse({'error': 'Detalle Factura must have a factura id'}, status=400)

    from django.shortcuts import get_object_or_404
    factura = get_object_or_404(Factura, pk=id)
    df = DetalleFactura(factura=factura)
    df.save()
    return JsonResponse({'success': True, 'id': df.id})


"""
  Servizo forestal to Detalle Factura association
"""
from django.views.decorators.http import require_http_methods

@staff_member_required
@require_http_methods(["POST"])
def assocservizodetalle(request):
    try:
        detalle = request.POST.get("detalle")
        servizo = request.POST.get("servizo")

        if not detalle or not servizo:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        from django.shortcuts import get_object_or_404
        servizoObj = get_object_or_404(Tala, pk=servizo)
        updated = DetalleFactura.objects.filter(pk=detalle).update(servizo=servizoObj)

        if updated:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Detalle not found'}, status=404)

    except Exception as e:
        logger.exception(f"Error in assocservizodetalle: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)


"""
  Related functions
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

@staff_member_required
def backup(request):
    """
    Performs database backup - requires staff member authentication
    """
    try:
        # Use absolute path and avoid shell=True for security
        backup_script = os.path.join(settings.BASE_DIR, 'backup_db.sh')

        # Check if script exists
        if not os.path.exists(backup_script):
            logger.error(f"Backup script not found: {backup_script}")
            return JsonResponse({
                'status': 'error',
                'message': 'Backup script not found'
            }, status=500)

        # Run without shell=True for security
        result = subprocess.run(
            ['/bin/bash', backup_script],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=settings.BASE_DIR
        )

        if result.returncode != 0:
            logger.error(f"Backup failed: {result.stderr}")
            return JsonResponse({
                'status': 'error',
                'message': 'Backup failed',
                'details': result.stderr
            }, status=500)

        logger.info("Backup completed successfully")
        return JsonResponse({
            'status': 'success',
            'message': 'Backup completed successfully',
            'output': result.stdout
        })

    except subprocess.TimeoutExpired:
        logger.error("Backup timed out")
        return JsonResponse({
            'status': 'error',
            'message': 'Backup process timed out'
        }, status=500)
    except Exception as e:
        logger.exception(f"Unexpected error during backup: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'An error occurred during backup'
        }, status=500)


"""
  Spreadsheet export
"""
@staff_member_required
def exportgrid(request):
    logger.debug(f"Export grid request: {request.POST}")
    return JsonResponse({'message': 'Export functionality not yet implemented'}, status=501)

