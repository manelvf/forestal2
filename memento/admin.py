from types import *
from django.contrib import admin
from django.core import serializers
from memento.models import Memento


def data_show(obj):
    s = u""
    for o in serializers.deserialize("json",obj.data):
        names = o.object._meta.get_all_field_names()
        for k in names:
            s += unicode(getattr(o.object, k))

    return (u"asdfsads").upper()

data_show.short_description = "Data Show"


class MementoAdmin(admin.ModelAdmin):
    list_display = ('app', 'model', "data_show", 'date','user')
    list_filter = ('app', 'model', 'date','user')

    def data_show(self, obj):
        s = u""
        for o in serializers.deserialize("json",obj.data):
            names = o.object._meta.get_all_field_names()
            print(names)
            for k in names:
                #if k[0:1] == "_": continue
                #print k
                q = hasattr(o.object, k)
                if q:
                    s += unicode(k) + u": " + unicode(getattr(o.object, k)) + u"<br />"

        return s

    data_show.short_description = "Data Show"
    data_show.allow_tags = True

admin.site.register(Memento, MementoAdmin)

