import React from 'react';
import { Scatter } from 'react-chartjs-2';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',');
  return parts[0] + ',' + parts[1];
}

class Sparkline extends React.Component {
  constructor(props) {
    super();
    this.state = { exchange: props.exchange, symbol: props.symbol, account: props.account };
    this.valueChartPoints = [];
    this.spendingChartPoints = [];
  }

  componentDidMount() {
    this.updateAmount(this.state.account);
  }

  updateAmount(account) {
    let url =
      'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/history/' +
      account +
      '/' +
      this.state.exchange +
      '/' +
      this.state.symbol;
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            valueData: this.processValue(result),
            account,
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        }
      );
    url =
      'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/spending/' +
      account +
      '/' +
      this.state.exchange +
      '/' +
      this.state.symbol;
    fetch(url)
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

  componentWillReceiveProps(nextProps) {
    this.updateAmount(nextProps.account);
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
      fill: true,
      // borderColor: mainColor,
      // backgroundColor: mainColor,
      // pointBorderColor: 'rgba(0,0,0,1)',
      // pointBorderWidth: 1,
      // pointHoverRadius: 8,
      // pointHoverBorderColor: 'rgba(0,0,0,1)',
      // pointHoverBorderWidth: 2,
      // pointRadius: showPoints ? 4 : 0,
      // pointHitRadius: 10,
      // pointStyle,
      showLine: true,
      // lineTension: 0,
      data: xyPoints,
    };
  }

  render() {
    return (
      <Scatter
        data={this.state}
        options={{
          responsive: false,
          title: {
            display: false,
          },
          legend: {
            display: false,
          },
          elements: {
            line: {
              borderColor: '#000000',
              borderWidth: 1,
            },
            point: {
              radius: 0,
            },
          },
          scales: {
            yAxes: [
              {
                display: false,
              },
            ],
            xAxes: [
              {
                display: false,
              },
            ],
          },
        }}
      />
    );
  }
}

export default Sparkline;
