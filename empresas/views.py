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

from forestal2.empresas.models import Empresa
from forestal2 import settings


def EmpresaSelect(request):
		
		empresas = Empresa.objects.all()
		r = json.dumps(empresas)

		return HttpResponse(r)


def facturagridview(request):
    return render_to_response("facturagridview.html",
        locals(), context_instance = RequestContext(request) )


def gridfactura(request):
    pass


def backup(request):
    try:
        r = subprocess.Popen(["./backup_db.sh", ], stdout=subprocess.PIPE, shell=True).communicate()[0]
    except:
        return HttpResponse(u"<b>There was an error on the backup process</b>")
        
    #r = subprocess.Popen(["./a.sh"], stdout=subprocess.PIPE, shell=True).communicate()[0]
    return HttpResponse(str(r) + "<p>Proceso completado")


