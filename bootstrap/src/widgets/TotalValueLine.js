import React from 'react';
import { Scatter } from 'react-chartjs-2';
import { Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',');
  return parts[0] + ',' + parts[1];
}

class TotalValueLine extends React.Component {
  constructor(props) {
    super();
    this.state = {
      account: props.account,
    };
    this.valueChartPoints = [];
    this.spendingChartPoints = [];
  }

  componentDidMount() {
    this.updateAmount(this.state.account);
  }

  updateAmount(account) {
    var url;
    if (account === 'all') {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/all_history';
    } else {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/history/' + account;
    }
    var t0 = performance.now();
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            valueData: this.processValueFillInBlanks(result),
          });
          var t1 = performance.now();
          console.log('Call to ' + url + ' took ' + (t1 - t0) + ' milliseconds.');
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
    if (account === 'all') {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/all_spending';
    } else {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/spending/' + account;
    }
    var t2 = performance.now();
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            spendingData: this.processSpendingFillInBlanks(result['spending']),
          });
          var t3 = performance.now();
          console.log('Call to ' + url + ' took ' + (t3 - t2) + ' milliseconds.');
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  static getDerivedStateFromProps(props, current_state) {
    if (current_state.account !== props.account) {
      return {
        account: props.account,
      };
    }
    return null;
  }

  processValue(data) {
    this.valueChartPoints = [];
    data.forEach((element) => {
      let point = {
        x: this.getDate(element['date']),
        y: element['value'],
      };
      this.valueChartPoints.push(point);
    });
    this.rebuildChart();
  }

  processValueFillInBlanks(data) {
    this.valueChartPoints = [];
    let actuals = {};
    let minDate = null;
    data.forEach((element) => {
      let thisDate = new Date(this.getDate(element['date']));
      actuals[thisDate] = element['value'];
      if (minDate == null || minDate > thisDate) {
        minDate = thisDate;
      }
    });
    if (minDate == null) {
      this.rebuildChart();
      return;
    }
    let total = 0;
    for (var d = minDate; d <= new Date(); d.setDate(d.getDate() + 1)) {
      let currentDate = d;
      if (currentDate in actuals) {
        total = actuals[currentDate];
      }
      let point = {
        x: this.getDate(currentDate),
        y: total,
      };
      this.valueChartPoints.push(point);
      currentDate = currentDate + 1;
    }
    this.rebuildChart();
  }

  processSpendingFillInBlanks(data) {
    this.spendingChartPoints = [];
    let actuals = {};
    let minDate = null;
    data.forEach((element) => {
      let thisDate = new Date(this.getDate(element['date']));
      actuals[thisDate] = element['total'];
      if (minDate == null || minDate > thisDate) {
        minDate = thisDate;
      }
    });
    if (minDate == null) {
      this.rebuildChart();
      return;
    }
    let total = 0;
    for (var d = minDate; d <= new Date(); d.setDate(d.getDate() + 1)) {
      let currentDate = d;
      if (currentDate in actuals) {
        total = total + actuals[currentDate];
      }
      let point = {
        x: this.getDate(currentDate),
        y: total,
      };
      this.spendingChartPoints.push(point);
      currentDate = currentDate + 1;
    }
    this.rebuildChart();
  }

  getDate(dateString) {
    return moment(dateString);
  }

  rebuildChart() {
    let chartData = {
      labels: ['Scatter'],
      datasets: [
        this.buildSeries('value', this.valueChartPoints, 'rgba(0,192,0,0.4)', false, null),
        this.buildSeries('spending', this.spendingChartPoints, 'rgba(192,0,0,0.4)', false, 'cross'),
      ],
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
      data: xyPoints,
    };
  }

  render() {
    return (
      <Card className="mb-1">
        <Scatter
          data={this.state}
          options={{
            title: {
              display: true,
              text: 'Spending vs Value',
              fontSize: 20,
            },
            legend: {
              display: false,
              position: 'right',
            },
            tooltips: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function (t, d) {
                  return formatDate(t.xLabel) + ' : $' + Math.round(t.value).toLocaleString();
                },
              },
            },
            scales: {
              xAxes: [
                {
                  type: 'time',
                  time: {
                    unit: 'day',
                  },
                  ticks: {
                    min: '2021-01-01',
                    max: new Date(),
                  },
                },
              ],
              yAxes: [
                {
                  ticks: {
                    callback: function (value, index, values) {
                      //return value.toLocaleString("en-US",{style:"currency", currency:"USD"});
                      return '$' + Math.round(value).toLocaleString();
                    },
                  },
                },
              ],
            },
          }}
        />
      </Card>
    );
  }
}

export default TotalValueLine;
