var servizoGridConf = {
        url:'{% url forestal2.fincas.views.grid %}',
        datatype: 'json',
        mtype: 'GET',
        colNames:['id','concello', 'poligon','parcela','Permiso','Comezo','Codigo'],
        colModel :[ 
          {name:'id', index:'id', width:55}, 
          {name:'concello', index:'concello', width:150}, 
          {name:'poligon', index:'poligon', width:80, align:'right'}, 
          {name:'parcela', index:'parcela', width:90, align:'right'}, 
          {name:'permiso', index:'permiso', width:140, align:"center"}, 
          {name:'comezo', index:'comezo', width:140, align:"center"},
          {name:'codigoPECL', index:'codigoPECL', width:140, align:"center"} 
        ],
        pager: '#pager',
        rowNum:20,
        rowList:[20,30],
        sortname: 'comezo',
        sortorder: 'asc',
        //viewrecords: true,
        caption: 'Servizos',
        height: 'auto'
}
