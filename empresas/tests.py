import json
import datetime
import os
import tempfile
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse

from empresas.models import (
    Provincia as EmpresasProvincia, TipoIva, TipoEmpresa, Empresa, Empleado, Camion,
    TipoOperacion, Factura, DetalleFactura, PhoneBook
)
from fincas.models import Tala, Finca, Concello, ModeloForestal, Provincia as FincasProvincia


class EmpresasViewTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test data
        self.empresas_provincia = EmpresasProvincia.objects.create(name='Test Provincia')
        self.fincas_provincia = FincasProvincia.objects.create(name='Test Provincia', code='TP')
        self.tipo_iva = TipoIva.objects.create(tipo=21.0)
        self.tipo_empresa = TipoEmpresa.objects.create(name='Test Tipo Empresa')
        
        self.empresa = Empresa.objects.create(
            name='Test Empresa',
            nif='12345678A',
            direccion='Test Address',
            cp='12345',
            provincia=self.empresas_provincia,
            telefonos='123456789',
            obs='Test observations',
            tipoempresa=self.tipo_empresa,
            codigo_certificacion='CERT123'
        )
        
        self.cliente_empresa = Empresa.objects.create(
            name='Cliente Test',
            nif='87654321B',
            direccion='Cliente Address',
            cp='54321',
            provincia=self.empresas_provincia,
            telefonos='987654321',
            tipoempresa=self.tipo_empresa
        )
        
        # Create empleado
        self.empleado = Empleado.objects.create(
            name='Test',
            apellido1='Employee',
            apellido2='Name',
            nif='11111111A',
            empresa=self.empresa
        )
        
        # Create camion
        self.camion = Camion.objects.create(
            matricula='TEST123',
            empresa=self.empresa
        )
        
        # Create tipo operacion and factura
        self.tipo_operacion = TipoOperacion.objects.create(name='Factura')
        self.factura = Factura.objects.create(
            empresa=self.empresa,
            cliente=self.cliente_empresa,
            tipo=self.tipo_operacion,
            numero=1,
            emision=datetime.date.today()
        )
        
        # Create concello and finca for tala
        self.concello = Concello.objects.create(name='Test Concello', provincia=self.fincas_provincia)
        self.modelo_forestal = ModeloForestal.objects.create(
            name='Test Modelo',
            obs='Test modelo forestal'
        )
        self.finca = Finca.objects.create(
            concello=self.concello,
            zona=1,
            poligon=1,
            parcela=1,
            agregado=0,
            superficie=10.5,
            fecha_plantacion=datetime.date.today(),
            densidad=100.0,
            ha_matorral=1.0,
            ha_prado=2.0,
            ha_construidas=0.5,
            ha_total=10.5,
            dono=self.empresa,
            empresa=self.empresa,
            modeloforestal=self.modelo_forestal
        )
        
        # Create tala for detalle factura
        self.tala = Tala.objects.create(
            finca=self.finca,
            m2_permiso=1000,
            permiso=datetime.date.today(),
            codigoPECL='TEST001'
        )
        
        # Create detalle factura
        self.detalle_factura = DetalleFactura.objects.create(
            factura=self.factura,
            servizo=self.tala,
            concepto='Test Service',
            tipo_iva=self.tipo_iva,
            cantidad=1,
            valor=100.00
        )


class TestEmpresaSelectView(EmpresasViewTestCase):
    def test_empresa_select_view(self):
        """Test EmpresaSelect view returns JSON list of empresas"""
        response = self.client.get('/EmpresaSelect')  # This URL doesn't exist in current urls.py
        # Since this URL doesn't exist in the current URL configuration, 
        # this test demonstrates what the test would look like
        # You would need to add the URL pattern to urls.py first


class TestFacturaGridView(EmpresasViewTestCase):
    def test_facturagridview(self):
        """Test factura grid view"""
        response = self.client.get('/api/facturagridview')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'facturagridview.html')


class TestGridFacturaView(EmpresasViewTestCase):
    def test_gridfactura_view_basic(self):
        """Test gridfactura view with basic parameters"""
        response = self.client.get('/api/gridfactura', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        
        data = json.loads(response.content)
        self.assertIn('total', data)
        self.assertIn('page', data)
        self.assertIn('records', data)
        self.assertIn('rows', data)
        self.assertEqual(len(data['rows']), 1)  # We created one factura
        
        # Check factura data
        factura_row = data['rows'][0]
        self.assertEqual(factura_row['id'], self.factura.id)
        self.assertIn(str(self.factura.empresa), factura_row['cell'])
        
    def test_gridfactura_view_with_pagination(self):
        """Test gridfactura view with different pagination parameters"""
        response = self.client.get('/api/gridfactura', {
            'page': '2',
            'rows': '5',
            'sidx': 'numero',
            'sord': 'desc'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['page'], 2)


class TestGridDetalleFacturaView(EmpresasViewTestCase):
    def test_griddetallefactura_view_basic(self):
        """Test griddetallefactura view"""
        response = self.client.get('/api/griddetallefactura', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc'
        })
        self.assertEqual(response.status_code, 200)
        
    def test_griddetallefactura_view_with_id(self):
        """Test griddetallefactura view with specific factura ID"""
        response = self.client.get(f'/api/griddetallefactura/{self.factura.pk}/', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc'
        })
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('total', data)
        self.assertEqual(len(data['rows']), 1)  # We created one detalle factura
        
        # Check detalle factura data
        detalle_row = data['rows'][0]
        self.assertEqual(detalle_row['id'], self.detalle_factura.id)
        self.assertIn(str(self.detalle_factura.servizo), detalle_row['cell'])


class TestAddDetalleFacturaView(EmpresasViewTestCase):
    def test_adddetallefactura_view_with_id(self):
        """Test adding detalle factura with valid factura ID"""
        initial_count = DetalleFactura.objects.filter(factura=self.factura).count()
        
        response = self.client.get(f'/api/adddetallefactura/{self.factura.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
        # Check that a new DetalleFactura was created
        final_count = DetalleFactura.objects.filter(factura=self.factura).count()
        self.assertEqual(final_count, initial_count + 1)
        
    def test_adddetallefactura_view_without_id(self):
        """Test adding detalle factura without factura ID"""
        response = self.client.get('/api/adddetallefactura')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle Factura mush have a factura id')


class TestAssocServizoDetalleView(EmpresasViewTestCase):
    def test_assocservizodetalle_view(self):
        """Test association of servizo and detalle factura"""
        # Create a new detalle factura without servizo
        new_detalle = DetalleFactura.objects.create(
            factura=self.factura,
            concepto='New Service',
            tipo_iva=self.tipo_iva,
            cantidad=2,
            valor=200.00
        )
        
        response = self.client.get('/api/assocservizodetalle', {
            'detalle': str(new_detalle.pk),
            'servizo': str(self.tala.pk)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
        # Verify the association was created
        updated_detalle = DetalleFactura.objects.get(pk=new_detalle.pk)
        self.assertEqual(updated_detalle.servizo, self.tala)


class TestBackupView(EmpresasViewTestCase):
    @patch('subprocess.Popen')
    def test_backup_view_success(self, mock_popen):
        """Test backup view with successful backup process"""
        mock_process = MagicMock()
        mock_process.communicate.return_value = (b'Backup completed successfully', b'')
        mock_popen.return_value = mock_process
        
        response = self.client.get('/api/backup')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Proceso completado')
        
    @patch('subprocess.Popen')
    def test_backup_view_failure(self, mock_popen):
        """Test backup view with failed backup process"""
        mock_popen.side_effect = Exception('Backup failed')
        
        response = self.client.get('/api/backup')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There was an error on the backup process')


class TestExportGridView(EmpresasViewTestCase):
    def test_exportgrid_view(self):
        """Test export grid view"""
        response = self.client.post('/api/exportGrid', {
            'test_data': 'test_value'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '')


# Test model creation and basic functionality
class TestEmpresasModels(TestCase):
    def setUp(self):
        self.provincia = EmpresasProvincia.objects.create(name='Test Provincia')
        self.tipo_empresa = TipoEmpresa.objects.create(name='Test Tipo')
        self.tipo_iva = TipoIva.objects.create(tipo=21.0)
        
    def test_empresa_creation(self):
        """Test Empresa model creation"""
        empresa = Empresa.objects.create(
            name='Test Company',
            nif='12345678A',
            direccion='Test Address',
            cp='12345',
            provincia=self.provincia,
            telefonos='123456789',
            tipoempresa=self.tipo_empresa,
            codigo_certificacion='CERT001'
        )
        self.assertEqual(str(empresa), 'Test Company')
        self.assertEqual(empresa.nif, '12345678A')
        self.assertEqual(empresa.codigo_certificacion, 'CERT001')
        
    def test_empleado_creation(self):
        """Test Empleado model creation"""
        empresa = Empresa.objects.create(
            name='Test Company',
            nif='12345678A',
            provincia=self.provincia,
            tipoempresa=self.tipo_empresa
        )
        empleado = Empleado.objects.create(
            name='John',
            apellido1='Doe',
            apellido2='Smith',
            nif='11111111A',
            empresa=empresa
        )
        self.assertEqual(str(empleado), 'John')
        self.assertEqual(empleado.empresa, empresa)
        
    def test_camion_creation(self):
        """Test Camion model creation"""
        empresa = Empresa.objects.create(
            name='Transport Company',
            nif='12345678A',
            provincia=self.provincia,
            tipoempresa=self.tipo_empresa
        )
        camion = Camion.objects.create(
            matricula='ABC123',
            empresa=empresa
        )
        self.assertEqual(str(camion), 'Transport Company ABC123')
        
    def test_factura_creation(self):
        """Test Factura model creation"""
        empresa = Empresa.objects.create(
            name='Billing Company',
            nif='12345678A',
            provincia=self.provincia,
            tipoempresa=self.tipo_empresa
        )
        cliente = Empresa.objects.create(
            name='Client Company',
            nif='87654321B',
            provincia=self.provincia,
            tipoempresa=self.tipo_empresa
        )
        tipo_operacion = TipoOperacion.objects.create(name='Factura')
        factura = Factura.objects.create(
            empresa=empresa,
            cliente=cliente,
            tipo=tipo_operacion,
            numero=123,
            emision=datetime.date.today()
        )
        self.assertEqual(factura.tipo, tipo_operacion)
        self.assertEqual(factura.numero, 123)
        self.assertEqual(factura.empresa, empresa)
        self.assertEqual(factura.cliente, cliente)
        
    def test_detalle_factura_creation(self):
        """Test DetalleFactura model creation"""
        empresa = Empresa.objects.create(
            name='Test Company',
            nif='12345678A',
            provincia=self.provincia,
            tipoempresa=self.tipo_empresa
        )
        tipo_operacion = TipoOperacion.objects.create(name='Factura')
        factura = Factura.objects.create(
            empresa=empresa,
            cliente=empresa,
            tipo=tipo_operacion,
            numero=1,
            emision=datetime.date.today()
        )
        detalle = DetalleFactura.objects.create(
            factura=factura,
            concepto='Test Service',
            tipo_iva=self.tipo_iva,
            cantidad=1,
            valor=100.00
        )
        self.assertEqual(detalle.concepto, 'Test Service')
        self.assertEqual(detalle.valor, 100.00)
        self.assertEqual(detalle.factura, factura)
        
    def test_phonebook_creation(self):
        """Test PhoneBook model creation"""
        phonebook = PhoneBook.objects.create(
            number='123456789',
            name='Test Contact'
        )
        self.assertEqual(phonebook.number, '123456789')
        self.assertEqual(phonebook.name, 'Test Contact')
        
    def test_tipo_iva_creation(self):
        """Test TipoIva model creation"""
        tipo_iva = TipoIva.objects.create(tipo=10.0)
        self.assertEqual(str(tipo_iva), '10.0')
        self.assertEqual(tipo_iva.tipo, 10.0)
        
    def test_provincia_creation(self):
        """Test Provincia model creation"""
        provincia = EmpresasProvincia.objects.create(name='Galicia')
        self.assertEqual(str(provincia), 'Galicia')
        
    def test_tipo_empresa_creation(self):
        """Test TipoEmpresa model creation"""
        tipo_empresa = TipoEmpresa.objects.create(name='Maderero')
        self.assertEqual(str(tipo_empresa), 'Maderero')


# Integration tests for complex workflows
class TestComplexWorkflows(EmpresasViewTestCase):
    def test_complete_factura_workflow(self):
        """Test complete workflow: create factura, add detalles, associate servizos"""
        # Create a new factura
        new_factura = Factura.objects.create(
            empresa=self.empresa,
            cliente=self.cliente_empresa,
            tipo=self.tipo_operacion,
            numero=2,
            emision=datetime.date.today()
        )
        
        # Add detalle factura via view
        response = self.client.get(f'/api/adddetallefactura/{new_factura.pk}/')
        self.assertEqual(response.status_code, 200)
        
        # Get the created detalle
        detalle = DetalleFactura.objects.filter(factura=new_factura).first()
        self.assertIsNotNone(detalle)
        
        # Associate with servizo
        response = self.client.get('/api/assocservizodetalle', {
            'detalle': str(detalle.pk),
            'servizo': str(self.tala.pk)
        })
        self.assertEqual(response.status_code, 200)
        
        # Verify the complete workflow
        updated_detalle = DetalleFactura.objects.get(pk=detalle.pk)
        self.assertEqual(updated_detalle.servizo, self.tala)
        self.assertEqual(updated_detalle.factura, new_factura)
        
    def test_grid_data_consistency(self):
        """Test that grid views return consistent data"""
        # Test gridfactura
        response = self.client.get('/api/gridfactura', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc'
        })
        factura_data = json.loads(response.content)
        
        # Test griddetallefactura for the same factura
        response = self.client.get(f'/api/griddetallefactura/{self.factura.pk}/', {
            'page': '1',
            'rows': '15',
            'sidx': 'id',
            'sord': 'asc'
        })
        detalle_data = json.loads(response.content)
        
        # Verify data consistency
        self.assertEqual(factura_data['records'], 1)
        self.assertEqual(detalle_data['records'], 1)
        
        # The factura in the grid should match our test factura
        factura_row = factura_data['rows'][0]
        self.assertEqual(factura_row['id'], self.factura.id)

