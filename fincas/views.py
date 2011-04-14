# -*- coding: utf-8 -*-
import sys

from django.http import HttpResponse
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from django.core.urlresolvers import resolve
from django.conf import settings

from suds import WebFault
from suds.client import Client

from forestal2.fincas.models import Finca, ViaxeCamion, Tala


jsFiles = [settings.ADMIN_MEDIA_PREFIX + "js/jquery.min.js"]

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
		
