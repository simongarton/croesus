import React from 'react';
import { Scatter } from 'react-chartjs-2';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',');
  return parts[0] + ',' + parts[1];
}

class GainLossLine extends React.Component {
  constructor(props) {
    super();
    this.state = { account: props.account };
    this.valueChartPoints = [];
    this.spendingChartPoints = [];
    this.gainAndLossChartPoints = [];
  }

  componentDidMount() {
    this.updateAmount(this.state.account);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ account: nextProps.account });
    this.updateAmount(nextProps.account);
  }

  updateAmount(account) {
    fetch('https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/history/' + account)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            valueData: this.processValueFillInBlanks(result),
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
    fetch('https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/spending/' + account)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            spendingData: this.processSpendingFillInBlanks(result['spending']),
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
  }

  processValueFillInBlanks(data) {
    this.valueChartPoints = [];
    let actuals = {};
    let minDate = null;
    data.forEach((element) => {
      let thisDate = new Date(moment(element['date']));
      actuals[thisDate] = element['value'];
      if (minDate == null || minDate > thisDate) {
        minDate = thisDate;
      }
    });
    let total = 0;
    for (var d = new Date(2021, 0, 1); d <= new Date(); d.setDate(d.getDate() + 1)) {
      let currentDate = d;
      if (currentDate in actuals) {
        total = actuals[currentDate];
      }
      let point = {
        x: moment(currentDate),
        y: total,
      };
      this.valueChartPoints.push(point);
    }
    this.buildGainAndLoss();
  }

  processSpendingFillInBlanks(data) {
    this.spendingChartPoints = [];
    let actuals = {};
    let minDate = null;
    data.forEach((element) => {
      let thisDate = new Date(moment(element['date']));
      actuals[thisDate] = element['total'];
      if (minDate == null || minDate > thisDate) {
        minDate = thisDate;
      }
    });
    let total = 0;
    for (var d1 = minDate; d1 < new Date(2021, 0, 1); d1.setDate(d1.getDate() + 1)) {
      let currentDate = d1;
      if (currentDate in actuals) {
        total = total + actuals[currentDate];
      }
    }
    for (var d = new Date(2021, 0, 1); d <= new Date(); d.setDate(d.getDate() + 1)) {
      let currentDate = d;
      if (currentDate in actuals) {
        total = total + actuals[currentDate];
      }
      let point = {
        x: moment(currentDate),
        y: total,
      };
      this.spendingChartPoints.push(point);
    }
    this.buildGainAndLoss();
  }

  buildGainAndLoss() {
    this.gainAndLossChartPoints = [];
    if (this.spendingChartPoints.length !== this.valueChartPoints.length) {
      this.rebuildChart();
      return;
    }

    if (this.spendingChartPoints.length === 0) {
      this.rebuildChart();
      return;
    }

    for (let i = 0; i < this.spendingChartPoints.length; i++) {
      let spending = this.spendingChartPoints[i];
      let value = this.valueChartPoints[i];
      console.log('thing', spending['y']);
      this.gainAndLossChartPoints.push({
        x: value['x'],
        y: value['y'] - spending['y'],
      });
    }

    this.rebuildChart();
  }

  rebuildChart() {
    let chartData = {
      labels: ['Scatter'],
      datasets: [this.buildSeries('gain and loss', this.gainAndLossChartPoints, 'rgba(0,0,100,0.6)', false, null)],
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
      <Scatter
        data={this.state}
        options={{
          title: {
            display: true,
            text: 'Gain and Loss',
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
                  max: '2021-07-01',
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
    );
  }
}

export default GainLossLine;
