"""
Test data fixtures for the Forestal application.
This module provides reusable test data creation functions.
"""

import datetime
from django.contrib.auth.models import User

from empresas.models import (
    Provincia, TipoIva, TipoEmpresa, Empresa, Empleado, Camion,
    Factura, DetalleFactura, PhoneBook
)
from fincas.models import (
    Concello, Parroquia, Lugar, Finca, ViaxeCamion, Tala,
    Deed, DeedSellers, DeedFinca, Unidade, ModeloForestal,
    Monte, BorderFinca, EventFincaType, EventFinca, EventFincaTimeline
)


def create_basic_test_data():
    """
    Creates basic test data that can be reused across tests.
    Returns a dictionary with all created objects.
    """
    data = {}
    
    # Create basic geographic data
    data['provincia'] = Provincia.objects.create(name='Test Provincia')
    data['concello'] = Concello.objects.create(
        name='Test Concello', 
        provincia=data['provincia']
    )
    data['parroquia'] = Parroquia.objects.create(
        name='Test Parroquia', 
        concello=data['concello']
    )
    data['lugar'] = Lugar.objects.create(
        name='Test Lugar', 
        parroquia=data['parroquia'], 
        concello=data['concello']
    )
    
    # Create business data
    data['tipo_iva'] = TipoIva.objects.create(tipo=21.0)
    data['tipo_empresa'] = TipoEmpresa.objects.create(name='Transporte')
    
    data['empresa'] = Empresa.objects.create(
        name='Test Empresa',
        nif='12345678A',
        direccion='Test Address',
        cp='12345',
        provincia=data['provincia'],
        telefonos='123456789',
        obs='Test observations',
        tipoempresa=data['tipo_empresa'],
        codigo_certificacion='CERT123'
    )
    
    data['cliente_empresa'] = Empresa.objects.create(
        name='Cliente Test',
        nif='87654321B',
        direccion='Cliente Address',
        cp='54321',
        provincia=data['provincia'],
        telefonos='987654321',
        tipoempresa=data['tipo_empresa']
    )
    
    # Create employee
    data['empleado'] = Empleado.objects.create(
        name='Test',
        apellido1='Employee',
        apellido2='Name',
        nif='11111111A',
        empresa=data['empresa']
    )
    
    # Create truck
    data['camion'] = Camion.objects.create(
        matricula='TEST123',
        empresa=data['empresa'],
        capacidade=10
    )
    
    # Create modelo forestal
    data['modelo_forestal'] = ModeloForestal.objects.create(
        name='Test Modelo',
        obs='Test modelo forestal'
    )
    
    # Create finca
    data['finca'] = Finca.objects.create(
        concello=data['concello'],
        zona=1,
        poligon=1,
        parcela=1,
        agregado=0,
        ha_total=10.5,
        dono=data['empresa'],
        empresa=data['empresa'],
        modeloforestal=data['modelo_forestal']
    )
    
    # Create tala
    data['tala'] = Tala.objects.create(
        finca=data['finca'],
        m2_permiso=1000,
        permiso=datetime.date.today(),
        comezo=datetime.date.today(),
        codigoPECL='TEST001',
        codigoNORFOR='NOR001'
    )
    
    # Create viaxe
    data['viaxe'] = ViaxeCamion.objects.create(
        dia=datetime.date.today(),
        camion=data['camion'],
        tm=5.0,
        destino=data['empresa'],
        n_talonario='TAL001',
        obs='Test observation'
    )
    data['viaxe'].origen.add(data['tala'])
    
    # Create factura
    data['factura'] = Factura.objects.create(
        empresa=data['empresa'],
        cliente=data['cliente_empresa'],
        tipo='F',
        numero='001',
        emision=datetime.date.today()
    )
    
    # Create detalle factura
    data['detalle_factura'] = DetalleFactura.objects.create(
        factura=data['factura'],
        servizo=data['tala'],
        concepto='Test Service',
        tipo_iva=data['tipo_iva'],
        cantidad=1,
        valor=100.00
    )
    
    return data


def create_user_data():
    """
    Creates test user data.
    Returns a dictionary with user objects.
    """
    return {
        'superuser': User.objects.create_superuser(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        ),
        'staff_user': User.objects.create_user(
            username='staffuser',
            email='staff@test.com',
            password='staffpass123',
            is_staff=True
        ),
        'regular_user': User.objects.create_user(
            username='regularuser',
            email='regular@test.com',
            password='regularpass123'
        )
    }


def create_complex_finca_data():
    """
    Creates more complex finca-related test data including deeds, events, etc.
    Returns a dictionary with the created objects.
    """
    basic_data = create_basic_test_data()
    
    # Create additional finca data
    data = {}
    data.update(basic_data)
    
    # Create monte
    data['monte'] = Monte.objects.create(
        parroquia=data['parroquia'],
        concello=data['concello'],
        lugar=data['lugar'],
        name='Test Monte',
        number=1
    )
    
    # Create border finca
    data['border_finca'] = BorderFinca.objects.create(
        concello=data['concello'],
        lugar=data['lugar'],
        poligon=2,
        parcela=2,
        agregado=1,
        zona=1,
        ref_catastral='12345ABCDE',
        obs='Border finca test'
    )
    
    # Create deed
    data['deed'] = Deed.objects.create(
        date=datetime.date.today(),
        number=1,
        buyer=data['empresa'],
        price=10000.00,
        deedType=1,  # COMPRAVENTA
        obs='Test deed'
    )
    
    # Create deed sellers
    data['deed_sellers'] = DeedSellers.objects.create(
        deed=data['deed'],
        empresa=data['cliente_empresa']
    )
    
    # Create deed finca relationship
    data['deed_finca'] = DeedFinca.objects.create(
        deed=data['deed'],
        finca=data['finca']
    )
    
    # Create event finca type
    data['event_finca_type'] = EventFincaType.objects.create(
        name='Test Event Type',
        order=1,
        obs='Test event type'
    )
    
    # Create event finca
    data['event_finca'] = EventFinca.objects.create(
        empresa=data['empresa'],
        date=datetime.date.today(),
        obs='Test event',
        eventType=data['event_finca_type']
    )
    
    # Create event finca timeline
    data['event_finca_timeline'] = EventFincaTimeline.objects.create(
        eventfinca=data['event_finca'],
        finca=data['finca']
    )
    
    return data


def create_multiple_test_objects():
    """
    Creates multiple instances of test objects for testing pagination, filtering, etc.
    Returns a dictionary with lists of created objects.
    """
    basic_data = create_basic_test_data()
    
    # Create multiple fincas
    fincas = []
    for i in range(5):
        finca = Finca.objects.create(
            concello=basic_data['concello'],
            zona=i + 1,
            poligon=i + 1,
            parcela=i + 1,
            agregado=0,
            ha_total=10.0 + i,
            dono=basic_data['empresa'],
            empresa=basic_data['empresa'],
            modeloforestal=basic_data['modelo_forestal']
        )
        fincas.append(finca)
    
    # Create multiple talas
    talas = []
    for i, finca in enumerate(fincas):
        tala = Tala.objects.create(
            finca=finca,
            m2_permiso=1000 + (i * 100),
            permiso=datetime.date.today(),
            codigoPECL=f'TEST{i:03d}',
            codigoNORFOR=f'NOR{i:03d}'
        )
        talas.append(tala)
    
    # Create multiple viaxes
    viaxes = []
    for i, tala in enumerate(talas):
        viaxe = ViaxeCamion.objects.create(
            dia=datetime.date.today(),
            camion=basic_data['camion'],
            tm=5.0 + i,
            destino=basic_data['empresa'],
            n_talonario=f'TAL{i:03d}',
            obs=f'Test observation {i}'
        )
        viaxe.origen.add(tala)
        viaxes.append(viaxe)
    
    # Create multiple facturas
    facturas = []
    for i in range(3):
        factura = Factura.objects.create(
            empresa=basic_data['empresa'],
            cliente=basic_data['cliente_empresa'],
            tipo='F',
            numero=f'{i:03d}',
            emision=datetime.date.today()
        )
        facturas.append(factura)
    
    # Create multiple detalle facturas
    detalle_facturas = []
    for i, factura in enumerate(facturas):
        for j in range(2):  # 2 detalles per factura
            detalle = DetalleFactura.objects.create(
                factura=factura,
                servizo=talas[j] if j < len(talas) else None,
                concepto=f'Service {i}-{j}',
                tipo_iva=basic_data['tipo_iva'],
                cantidad=j + 1,
                valor=100.00 * (j + 1)
            )
            detalle_facturas.append(detalle)
    
    return {
        'basic_data': basic_data,
        'fincas': fincas,
        'talas': talas,
        'viaxes': viaxes,
        'facturas': facturas,
        'detalle_facturas': detalle_facturas
    }