# -*- coding: utf-8 -*-
from types import *
from random import randint, random
from django.apps import apps
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.db.models.fields import CharField, IntegerField, FloatField


def schred(request):
    list = getModelList("empresas")

    for model in list:
        schredModel(model)

    return HttpResponse("OK")


def getModelList(app):
    return apps.get_models()

def schredModel(model):
    objects = model.objects.all();

    j = 0
    for o in objects:

        for f in o._meta.fields:

            if isinstance(f, CharField):

                s = u""
                v = f._get_val_from_obj(o)
                for c in unicode(v):
                    if c > 'a' and c < 'z':
                        c = chr(randint(97,122))
                    elif c > 'A' and c < 'Z':
                        c = chr(randint(65,90))
                    elif c > '0' and c < '9':
                        c = chr(randint(48,57))
                    else:
                        continue
                    s = s + c

                setattr(o, f.name, s)

            elif isinstance(f,IntegerField):
                setattr(o, f.name, randint(0,100000))

            elif type(f) == FloatField:
                setattr(o, f.name, randint(0,100) * random())
            else:
                pass

        o.save()




def is_numeric(var):
    try:
        float(var)
        return True
    except ValueError:
        return False



