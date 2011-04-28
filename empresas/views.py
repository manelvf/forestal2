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

from forestal2.empresas.models import Empresa


def EmpresaSelect(request):
		
		empresas = Empresa.objects.all()
		r = json.dumps(empresas)

		return HttpResponse(r)

