var detalleFacturaGridConf = {
                    datatype: "json",
                    colNames: ['id', 'servizo', 'concepto', 'tipo_iva', 'tipo_irpf', 'cantidad', 'valor'],
                    colModel: [{
                        name: 'id',
                        index: 'id',
                        width: 60
                    }, {
                        name: 'servizo',
                        index: 'servizo',
                        width: 200
                    }, {
                        name: 'concepto',
                        index: 'concepto',
                        width: 200,
                        align: 'right'
                    }, {
                        name: 'tipo_iva',
                        index: 'tipo_iva',
                        width: 50,
                        align: 'right'
                    }, {
                        name: 'tipo_irpf',
                        index: 'tipo_irpf',
                        width: 50,
                        align: "center"
                    }, {
                        name: 'cantidad',
                        index: 'cantidad',
                        width: 80,
                        align: "center"
                    }, {
                        name: 'valor',
                        index: 'valor',
                        width: 100,
                        align: "center"
                    }],
                    caption: "Detalle",
                    height: "auto",
                    rowNum: 15,
                    sortname: 'id',
                    sortorder: "asc"
}
