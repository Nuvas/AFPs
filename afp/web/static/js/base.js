google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(loadData);

function loadData() {
    $('.fund').each(function(){
        var myData = { id: $(this).find('.fund-title').attr('data-id') };
        $.ajax({ url: '/fondo/chart-data'
                , data: myData
                , dataType: 'json'
                , success: function(data, textStatus, jqXHR) {
                    for ( index in data.rows ) {
                        data.rows[index]['c'][0]['v'] = new Date(data.rows[index]['c'][0]['v']);
                    }
                    var data = new google.visualization.DataTable(data); 
                    var chart = new google.visualization.LineChart(document.getElementById('chart'+myData.id));
                    chart.draw(data, {width: 400, height: 240, chartArea:{left:45, width:380}, title: 'Variación del fondo en pesos.', legend: {position:'none'}});
                }
            });
    });
}
