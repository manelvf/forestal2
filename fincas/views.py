# Create your views here.
from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve

from forestal2.fincas.models import Finca, ViaxeCamion, Tala


"""
Check that every viaxecamion has one exactly Finca
"""
def homogeneidade(request):
    s = ""

    v = ViaxeCamion.objects.filter( Q(origen__isnull=True) 
                                 or Q(origen__isblank=True))
    
    listaCamions = v
    s = "" #resolve("/fincas/viaxecamion")

    return render_to_response("homogeneidade.html",
        {"listaCamions":listaCamions, "s":s} )
    
