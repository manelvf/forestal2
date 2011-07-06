var facturaGridConf = {
    datatype: "json",
    colNames: ['id', 'empresa', 'cliente', 'tipo', 'numero', 'emision'],
    colModel: [{
        name: 'id',
        index: 'id',
        width: 50
    }, {
        name: 'empresa',
        index: 'empresa',
        width: 200
    }, {
        name: 'cliente',
        index: 'cliente',
        width: 200,
    }, {
        name: 'tipo',
        index: 'tipo',
        width: 150,
        align: 'right'
    }, {
        name: 'numero',
        index: '',
        width: 90,
        align: "center"
    }, {
        name: 'emision',
        index: 'emision',
        width: 100,
        align: "center"
    }],
    caption: "Facturas",
    height: "auto",
    rowNum: 15,
    sortname: 'id',
    sortorder: "asc",
    pager: '#pager2',
};
