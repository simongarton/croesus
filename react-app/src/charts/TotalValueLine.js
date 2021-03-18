import React from 'react';
import {
  Scatter
} from 'react-chartjs-2';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',')
  return parts[0] + ',' + parts[1];
}

class TotalValueColumn extends React.Component {

  constructor(props) {
    super();
    this.state = {};
    this.valueChartPoints = [];
    this.spendingChartPoints = []
  }

  componentDidMount() {
    fetch("https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/history")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            valueData: this.processValue(result)
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
    fetch("https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/spending")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            spendingData: this.processSpending(result)
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )

  }

  processValue(data) {
    this.valueChartPoints = [];
    data.forEach(element => {
      let point = {
        'x': moment(element['date']),
        'y': element['value'],
      }
      this.valueChartPoints.push(point)
    });
    this.rebuildChart();
  }

  processSpending(data) {
    this.spendingChartPoints = [];
    let total = 0;
    data.forEach(element => {
      total = total + element['total'];
      let point = {
        'x': moment(element['date']),
        'y': total,
      }
      this.spendingChartPoints.push(point)
    });
    this.rebuildChart();
  }

  rebuildChart() {
    console.log(this.valueChartPoints);
    console.log(this.spendingChartPoints);

    let chartData = {
      labels: ['Scatter'],
      datasets: [
        this.buildSeries('value', this.valueChartPoints, 'rgba(0,192,0,0.4)', false, null),
        this.buildSeries('spending', this.spendingChartPoints, 'rgba(192,0,0,0.4)', true, 'cross')
      ]
    };
    this.setState(chartData);
  }

  buildSeries(label, xyPoints, mainColor, showPoints, pointStyle) {
    return {
      label: label,
      fill: false,
      borderColor: mainColor,
      backgroundColor: mainColor,
      pointBorderColor: 'rgba(0,0,0,1)',
      pointBorderWidth: 1,
      pointHoverRadius: 8,
      pointHoverBorderColor: 'rgba(0,0,0,1)',
      pointHoverBorderWidth: 2,
      pointRadius: showPoints ? 4 : 0,
      pointHitRadius: 10,
      pointStyle,
      showLine: true,
      lineTension: 0,
      data: xyPoints
    }
  }

  render() {
    return <Scatter
    data = {
      this.state
    }
    options = {
      {
        title: {
          display: true,
          text: 'Spending vs Value',
          fontSize: 20
        },
        legend: {
          display: false,
          position: 'right'
        },
        tooltips: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: function (t, d) {
              return formatDate(t.xLabel) + ' : $' + Math.round(t.value).toLocaleString();
            }
          }
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              unit: 'day'
            },
            ticks: {
              min: '2020-12-01',
              max: '2021-07-01'
            }

          }],
          yAxes: [{
            ticks: {
              callback: function (value, index, values) {
                //return value.toLocaleString("en-US",{style:"currency", currency:"USD"});
                return '$' + Math.round(value).toLocaleString();
              }
            }
          }]
        }
      }
    }
    />

  }
}

export default TotalValueColumn;