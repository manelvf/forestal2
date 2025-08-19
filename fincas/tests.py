import json
import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse

from fincas.models import (
    Concello, Parroquia, Lugar, Finca, ViaxeCamion, Tala,
    Deed, DeedSellers, DeedFinca, Unidade, ModeloForestal,
    Monte, BorderFinca, EventFincaType, EventFincaLog,
    EventFinca, EventFincaTimeline, Provincia as FincasProvincia
)
from empresas.models import Empresa, TipoEmpresa, TipoOperacion, Camion, Provincia as EmpresasProvincia


class FincasViewTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create superuser for staff-required views
        self.user = User.objects.create_superuser(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.client = Client()
        
        # Create test data
        self.fincas_provincia = FincasProvincia.objects.create(name='Test Provincia', code='TP')
        self.empresas_provincia = EmpresasProvincia.objects.create(name='Test Provincia')
        self.concello = Concello.objects.create(name='Test Concello', provincia=self.fincas_provincia)
        self.parroquia = Parroquia.objects.create(name='Test Parroquia', concello=self.concello)
        self.lugar = Lugar.objects.create(name='Test Lugar', parroquia=self.parroquia, concello=self.concello)
        
        # Create empresa and related objects
        self.tipo_empresa = TipoEmpresa.objects.create(name='Transporte')
        self.empresa = Empresa.objects.create(
            name='Test Empresa',
            nif='12345678A',
            provincia=self.empresas_provincia,
            tipoempresa=self.tipo_empresa
        )
        self.camion = Camion.objects.create(matricula='TEST123', empresa=self.empresa)
        
        # Create modelo forestal for finca
        self.modelo_forestal = ModeloForestal.objects.create(
            name='Test Modelo',
            obs='Test modelo forestal'
        )
        
        # Create finca
        self.finca = Finca.objects.create(
            concello=self.concello,
            zona=1,
            poligon=1,
            parcela=1,
            agregado=0,
            ha_total=10.5,
            dono=self.empresa,
            empresa=self.empresa,
            modeloforestal=self.modelo_forestal
        )
        
        # Create tala
        self.tala = Tala.objects.create(
            finca=self.finca,
            m2_permiso=1000,
            permiso=datetime.date.today(),
            comezo=datetime.date.today(),
            codigoPECL='TEST001',
            codigoNORFOR='NOR001'
        )
        
        # Create viaxe
        self.viaxe = ViaxeCamion.objects.create(
            dia=datetime.date.today(),
            camion=self.camion,
            tm=5.0,
            destino=self.empresa,
            n_talonario='TAL001',
            obs='Test observation'
        )
        self.viaxe.origen.add(self.tala)


class TestHomogeneidadeView(FincasViewTestCase):
    def test_homogeneidade_view_staff_required(self):
        """Test that homogeneidade view requires staff permission"""
        response = self.client.get('/api/homogeneidade/test/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_homogeneidade_view_with_staff(self):
        """Test homogeneidade view with staff user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/homogeneidade/test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Empresa')


class TestServizogridView(FincasViewTestCase):
    def test_servizogridview_staff_required(self):
        """Test that servizogridview requires staff permission"""
        response = self.client.get('/api/servizogridview')
        self.assertEqual(response.status_code, 302)
        
    def test_servizogridview_with_staff(self):
        """Test servizogridview with staff user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/servizogridview')
        self.assertEqual(response.status_code, 200)


class TestAssignFincaView(FincasViewTestCase):
    def test_assignfinca_view(self):
        """Test assignfinca view"""
        response = self.client.get(f'/api/assignfinca/{self.viaxe.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.viaxe))


class TestGridViews(FincasViewTestCase):
    def test_grid_view_basic(self):
        """Test grid view with basic parameters"""
        response = self.client.get('/api/grid/', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc',
            '_search': 'false'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        
        data = json.loads(response.content)
        self.assertIn('total', data)
        self.assertIn('page', data)
        self.assertIn('records', data)
        self.assertIn('rows', data)
        
    def test_grid_view_with_search(self):
        """Test grid view with search parameters"""
        filters = json.dumps({
            "groupOp": "AND",
            "rules": [{"field": "id", "op": "eq", "data": str(self.tala.pk)}]
        })
        response = self.client.get('/api/grid/', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc',
            '_search': 'true',
            'filters': filters
        })
        self.assertEqual(response.status_code, 200)
        
    def test_gridfinca_view(self):
        """Test gridfinca view"""
        response = self.client.get('/api/gridfinca', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc',
            '_search': 'false'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('total', data)
        self.assertEqual(len(data['rows']), 1)
        
    def test_gridviaxe_view(self):
        """Test gridviaxe view"""
        response = self.client.get('/api/gridviaxe', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc',
            'restriction': 'all',
            '_search': 'false'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('total', data)
        
    def test_gridviaxe_with_servizo(self):
        """Test gridviaxe view with specific servizo"""
        response = self.client.get(f'/api/gridviaxe/{self.tala.pk}/', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc',
            'restriction': 'all',
            '_search': 'false'
        })
        self.assertEqual(response.status_code, 200)


class TestAssociationViews(FincasViewTestCase):
    def test_assocfincaservizo_view(self):
        """Test association of finca and servizo"""
        response = self.client.get('/api/assocfincaservizo', {
            'finca': str(self.finca.pk),
            'servizo': str(self.tala.pk)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
    def test_assocservizocamion_view(self):
        """Test association of servizo and camion"""
        response = self.client.get('/api/assocservizocamion', {
            'servizo': str(self.tala.pk),
            'viaxe': str(self.viaxe.pk)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
    def test_desassocviaxeservizo_view(self):
        """Test disassociation of viaxe and servizo"""
        response = self.client.get('/api/desassocviaxeservizo', {
            'servizo': str(self.tala.pk),
            'viaxe': str(self.viaxe.pk)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
    def test_joinviaxefinca_view(self):
        """Test joining viaxe and finca"""
        response = self.client.get('/api/joinviaxefinca', {
            'idviaxe': str(self.viaxe.pk),
            'idtala': str(self.tala.pk),
            'action': 'ligar'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')


class TestListaViaxesView(FincasViewTestCase):
    def test_listaviaxes_view(self):
        """Test listaviaxes view"""
        response = self.client.get(f'/api/listaviaxes/{self.tala.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.viaxe.camion))


class TestLandQueryViews(FincasViewTestCase):
    def test_queryland_view_no_params(self):
        """Test queryland view without parameters"""
        response = self.client.get('/api/queryland')
        self.assertEqual(response.status_code, 200)
        
    def test_queryland_view_with_params(self):
        """Test queryland view with parameters (will fail without SOAP service)"""
        # This test demonstrates how the view would be called
        # In a real environment, you'd mock the SOAP service
        response = self.client.get('/api/queryland/provincia/concello/1/1')
        # Expected to return an error template due to missing SOAP service
        self.assertEqual(response.status_code, 200)


class TestWeightActionViews(FincasViewTestCase):
    def test_weightactions_view_staff_required(self):
        """Test that weightActions view requires staff permission"""
        response = self.client.get('/api/weightactions/')
        self.assertEqual(response.status_code, 302)
        
    def test_weightactions_view_with_staff(self):
        """Test weightActions view with staff user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/api/weightactions/')
        self.assertEqual(response.status_code, 200)
        
    def test_weightactionsoutput_view_with_staff(self):
        """Test weightActionsOutput view with staff user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/api/weightactionsoutput/', {
            'comezo': '2023-01-01',
            'final': '2023-12-31'
        })
        self.assertEqual(response.status_code, 200)


class TestCSVGenerationViews(FincasViewTestCase):
    def setUp(self):
        super().setUp()
        # Create additional test data for CSV generation
        self.deed = Deed.objects.create(
            date=datetime.date.today(),
            number=1,
            buyer=self.empresa,
            deedType=1,
            price=10000.00
        )
        self.deed_finca = DeedFinca.objects.create(deed=self.deed, finca=self.finca)
        self.deed_seller = DeedSellers.objects.create(deed=self.deed, empresa=self.empresa)
        
    def test_generatedeedcsv_view(self):
        """Test CSV generation for deeds"""
        response = self.client.get('/api/generateDeedCSV')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total:')


class TestUtilityViews(FincasViewTestCase):
    def test_rewritelandsize_view(self):
        """Test rewriteLandSize view (will fail without SOAP service)"""
        response = self.client.get('/api/rewriteLandSize')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')


# Test model creation and basic functionality
class TestFincasModels(TestCase):
    def setUp(self):
        self.provincia = Provincia.objects.create(name='Test Provincia', code='TP')
        self.concello = Concello.objects.create(name='Test Concello', provincia=self.provincia)
        self.tipo_empresa = TipoEmpresa.objects.create(name='Test Tipo')
        self.empresa = Empresa.objects.create(
            name='Test Empresa',
            nif='12345678A',
            provincia=self.empresas_provincia,
            tipoempresa=self.tipo_empresa
        )
        
    def test_finca_creation(self):
        """Test Finca model creation"""
        modelo_forestal = ModeloForestal.objects.create(
            name='Test Modelo',
            obs='Test modelo forestal'
        )
        finca = Finca.objects.create(
            concello=self.concello,
            zona=1,
            poligon=1,
            parcela=1,
            agregado=0,
            ha_total=10.5,
            dono=self.empresa,
            empresa=self.empresa,
            modeloforestal=modelo_forestal
        )
        self.assertEqual(str(finca), f'1-1-1')
        self.assertEqual(finca.ha_total, 10.5)
        
    def test_tala_creation(self):
        """Test Tala model creation"""
        modelo_forestal = ModeloForestal.objects.create(
            name='Test Modelo',
            obs='Test modelo forestal'
        )
        finca = Finca.objects.create(
            concello=self.concello,
            zona=1,
            poligon=1,
            parcela=1,
            agregado=0,
            ha_total=10.5,
            dono=self.empresa,
            empresa=self.empresa,
            modeloforestal=modelo_forestal
        )
        tala = Tala.objects.create(
            finca=finca,
            m2_permiso=1000,
            permiso=datetime.date.today(),
            codigoPECL='TEST001'
        )
        self.assertEqual(tala.m2_permiso, 1000)
        self.assertEqual(tala.codigoPECL, 'TEST001')
        
    def test_viaxecamion_creation(self):
        """Test ViaxeCamion model creation"""
        camion = Camion.objects.create(matricula='TEST123', empresa=self.empresa, capacidade=10)
        viaxe = ViaxeCamion.objects.create(
            dia=datetime.date.today(),
            camion=camion,
            tm=5.0,
            destino=self.empresa,
            n_talonario='TAL001'
        )
        self.assertEqual(viaxe.tm, 5.0)
        self.assertEqual(viaxe.n_talonario, 'TAL001')

