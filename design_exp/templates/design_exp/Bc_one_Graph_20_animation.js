/// First, this formats the data from Excel to be used in the graph

        //var DataFund = {{ array1 }}.map(x => x * 100);  // Convert proportions to percentages for Fund data
        //var DataBenchmark = {{ array2 }}.map(x => x * 100);  // Convert proportions to percentages for Benchmark data

        var DataFund = {{ array1 }}
        var DataBenchmark = {{ array2 }}
        var chartFund = [];  // initialize an empty array
        for(var i = 0; i < 0; i++) {
        chartFund.push([i, DataFund[i]]);  // add a pair [i, DataFund[i]] to the array
        }

        var chartBenchmark = [];  // initialize an empty array
        for(var i = 0; i < 0; i++) {
        chartBenchmark.push([i, DataBenchmark[i]]);  // add a pair [i, DataBenchmark[i]] to the array
        }
        var maxValue = {{ max_value }} *100; // Get maximum value for the player
        var minValue = - maxValue;

        var absMaxFund = Math.max(...DataFund.map(Math.abs)); // Get absolute maximum from DataFund
        var absMaxBenchmark = Math.max(...DataBenchmark.map(Math.abs)); // Get absolute maximum from DataBenchmark

        var dynamicMaxValue = Math.max(absMaxFund, absMaxBenchmark); // Choose the larger of the two
        var dynamicMinValue = Math.max(-dynamicMaxValue, -100); // Symmetric minimum value


var myChart; // Global variable to store the chart instance

var currentYear = 0; // Initialize the current year

// Update chart data function
function updateChartData() {

    if (currentYear < Math.min(DataFund.length, DataBenchmark.length)) {
        // Clear existing series data
        myChart.series[0].setData([], true);
        myChart.series[1].setData([], true);

        // Add data points for the current year
        var ChartFund = [[currentYear, DataFund[currentYear]]];
        var ChartBenchmark = [[currentYear, DataBenchmark[currentYear]]];

        // Update the chart with the current data point
        myChart.series[0].setData(ChartFund, false); // Update Fund series
        myChart.series[1].setData(ChartBenchmark, false); // Update Benchmark series

        // Update x-axis to display only the current year
        myChart.xAxis[0].update({
            min: currentYear,
            max: currentYear
        });

        currentYear++; // Increment the current year if it's not the last year
    }
    else {
        document.getElementById('explain_text').style.display = 'none'; // Hide the text
        document.getElementById('canvas').style.display = 'none'; // Hide the chart area
        document.getElementById('bb1').style.display = 'none'; // Hide the update button
        document.getElementById("choose_text").style.display = "block";
        document.getElementById("form-area").style.display = "block";
        //document.getElementById('b1').style.display = 'block'; // Show the Next button
        //document.getElementById('b1').disabled = false; // Enable the Next button
    }

    //var year = currentYear; // Update title year
    //myChart.setTitle({ text: 'Year ' + year });
}

/// Then, this creates the graph
function createChart() {
    myChart = Highcharts.chart('contr2', {
        chart: {
            backgroundColor: '#f8f9fa',
            type: 'column',
            width: 400,
            height: 400,
            marginLeft: 110,
            marginRight: 1,
            marginBottom: 100,
            marginf: 55,
//            events: {
//                load: function () {
//                    setTimeout(() => {
//                        animationComplete = true;
//                    }, animationtime/10);
//                }
//            }
        },
        title: {
            text: ''
        },
/*        title: {
             text: 'Year',
             align: 'left',
            x: 200
        },
*/
        xAxis: {
            type: 'linear',
            labels: {
                style: {
                    fontSize: '18px'
                },
                enabled:true,
                formatter: function() {
                    var year = currentYear + 1; // Add 1 to the current year to start from year 1
                    return 'Year ' + year;
                }
            },
            gridLineWidth: 1,
            pointPlacement: 'on',
            animation: false,
        },
        yAxis: {
            title: {
                text: "{{ yAxisLabel }}",
                margin: 15,
                style: {
                    fontSize: '18px',
                    width: '200px',
                    whiteSpace: 'wrap'
                }
            },
            labels: {
                style: {
                    fontSize: '14px'
                },
                enabled:true,
                formatter: function(){
                    return this.value + '%';
                }
            },
            min: dynamicMinValue,
            max: dynamicMaxValue,
            //tickInterval: 10,
            plotLines: [{
                color: 'black',
                width: 1,
                value: 0,
                zIndex: 2
            }],
            lineWidth: 1,
            tickWidth: 1,
            tickLength: 5,
            opposite: false
        },
        plotOptions: {
            series: {
                borderColor: 'transparent',
                animation: false,
                lineWidth: 3,
                states: {
                    hover: {
                        lineWidth: 3,
                        marker: {
                            enabled: true
                        }
                    }
                },
                events: {
                    legendItemClick: function() {
                        return false;
                    }
                }
            },
            column: {
                pointPlacement: 'between',
                animation: false,
                events: {
                    legendItemClick: function () {
                        return false;
                    }
                },
                pointWidth: 50,
                dataLabels: {
                    style: {
                        fontSize: '8px'
                    },
                    enabled: false,
                    formatter: function() {
                        return this.y.toFixed(1)+'%';
                    }
                }
            }
        },
        credits: {
            enabled: false
        },
        tooltip: {
            formatter: function () {
                // var year = this.x+1
                // var s = 'Year ' + year + '<br>';
                return this.points.reduce(function (s, point) {
                    return s + '<br/>' + point.series.name + ': <b>' +
                        Highcharts.numberFormat(point.y, 1, '.', ',') + '%'+'</b>'
                }, '<b>' + "Year " + (this.x+1) + '</b>');
            },
            shared: true
        },
        /*tooltip: {
            shared: true,
            formatter: function () {
                console.log("function called")
                if (!animationComplete) {
                    return false;
                } else {
                var year = this.x+1
                var s = 'Year ' + year + '<br>';
                $.each(this.points, function(i, point) {
                    s += this.series.name + ': <b>' + Highcharts.numberFormat(point.y, 1, '.', ',') + '%'+'</b><br>';
                });
                return s;
                }
            }
        },
        */
        legend: {
            align: 'center',
            enabled: true,
            squareSymbol: false,
            symbolHeight: 10,
            symbolWidth: 10,
            x: 45,
            y: 20, // Increase this value to move the legend down
            zIndex: 100,
            floating: true,
            backgroundColor: '#f8f9fa',
            shadow: false,
            itemStyle: {
                fontSize: '20px' // Increase the font size of the legend
            }
        },
        exporting: {
            enabled: false
        },
        series: [
        {
            name: 'Asset A',
            data: chartFund,
            color: '#00BFFF',
            pointPlacement: 'on',
            clip: false,
            zIndex: 1,
            id: 'main',
            pointPlacement: -0.04,
            pointRange: 1,
        },
        {
            name: 'Asset B',
            data: chartBenchmark,
            color: '#808080',
            pointPlacement: 'on',
            clip: false,
            zIndex: 0,
            pointPlacement: 0.04,
            pointRange: 1,
        },
        ]
    });
updateChartData();
}


// Initial call to create the chart with the first data point
createChart();

document.getElementById('updateChartButton').addEventListener('click', function() {
    updateChartData(); // Update chart data
});

// Set the interval to call incrementDataPoints every second
<!--var intervalId = setInterval(updateChartData, animationtime/10);-->