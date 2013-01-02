from django.test import TestCase
from forestal2.memento.views import getModelList, schredModel


class SchredderTestCase(TestCase):

    fixtures = ['empresas.json']

    def testgetModelList(self):
        list = getModelList("fincas")
        list = getModelList("empresas")

        self.assertTrue(len(list)>1)

        for model in list:
            schredModel(model)

    




        

