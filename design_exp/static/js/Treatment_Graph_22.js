function renderFundChart(containerId, DataFund, DataBenchmark) {
    // Split the string into an array and convert each element to a number
    var fundDataArray = DataFund.split(';').map(Number);
    var benchmarkDataArray = DataBenchmark.split(';').map(Number);

    // Convert data to chart format
    var chartFund = fundDataArray.map((value, index) => [index, value]);
    var chartBenchmark = benchmarkDataArray.map((value, index) => [index, value]);

    // Initialize Highcharts
    Highcharts.chart(containerId, {
        chart: {
            type: 'line',
        },
        title: {
            text: 'Hypothetical Growth of £10,000'
        },
        xAxis: {
            type: 'linear',
            title: {
                text: 'Year'
            },
            labels: {
                formatter: function () {
                    return Math.floor(this.value);
                }
            },
            tickInterval: 1
        },
        yAxis: {
            min: 0, // Minimum value set to 0
            title: {
                text: 'Value (£)'
            },
            tickInterval: 10000,
            labels: {
                formatter: function () {
                    return Highcharts.numberFormat(this.value, 0, '.', ',');
                }
            },
            lineWidth: 1,
            tickWidth: 1,
            tickLength: 5,
            opposite: true
        },
        tooltip: {
            shared: true,
            formatter: function () {
                var s = 'Year ' + Math.floor(this.x) + '<br>';
                $.each(this.points, function(i, point) {
                    s += point.series.name + ': <b>£' + Highcharts.numberFormat(point.y, 2, '.', ',') + '</b><br>';
                });
                return s;
            }
        },
        series: [
            {
                name: 'Fund',
                data: chartFund,
                color: '#00BFFF',
                zIndex: 1
            },
            {
                name: 'Benchmark',
                data: chartBenchmark,
                color: '#808080',
                zIndex: 0,
                dashStyle: 'ShortDash'
            }
        ],
        exporting: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                animation: false, // Disable animation
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
                        return false; // Prevents hiding series by clicking on legend
                    }
                }
            }
        }
    });
}
