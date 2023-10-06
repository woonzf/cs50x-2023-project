/* Google 3D Pie Chart */
google.charts.load("current", {packages:["corechart"]});

google.charts.setOnLoadCallback(drawgchartyear);
google.charts.setOnLoadCallback(drawgchartmonth);

function drawgchartyear() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Month');
    data.addColumn('number', 'Amount');
    for (var i = 0; i < months.length; i++) {
        data.addRow([months[i]["month"], yeardata[i]]);
    }

    var text1 = 'Year';
    var text2 = year;
    var options = {
        title: text1.concat(' ').concat(text2),
        is3D: true,
        fontSize: 18,
        height: 350,
        width: 700,
    };

    var chart = new google.visualization.PieChart(document.getElementById('gchartyear'));
    chart.draw(data, options);
}

function drawgchartmonth() {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Type');
    data.addColumn('number', 'Amount');
    for (var i = 0; i < types.length; i++) {
        data.addRow([types[i], monthdata[month][i]]);
    }

    var text1 = months[month-1].month;
    var text2 = year;
    var options = {
        title: text1.concat(' ').concat(text2),
        is3D: true,
        fontSize: 18,
        height: 350,
        width: 700,
    };

    var chart = new google.visualization.PieChart(document.getElementById('gchartmonth'));
    chart.draw(data, options);
}

document.addEventListener('DOMContentLoaded', function() {

    /* Filter button enabled if year is selected */
    let year = document.getElementById('year');
    year.addEventListener('click', function() {
        if (year.value != "") {
            document.getElementById('filter').disabled = false;
        }
    });
});
