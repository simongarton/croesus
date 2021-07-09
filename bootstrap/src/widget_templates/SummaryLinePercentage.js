import React from 'react';
import { Scatter } from 'react-chartjs-2';
import 'bootstrap/dist/css/bootstrap.min.css';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',');
  return parts[0] + ',' + parts[1];
}

class SummaryLinePercentage extends React.Component {
  constructor(props) {
    super();
    this.state = {
      title: props.title,
      field: props.field,
      mobile: props.mobile,
    };
    this.valueChartPoints = [];
    console.log(props);
  }

  componentDidMount() {
    var url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/summary/history';
    var t0 = performance.now();
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({
            isLoaded: true,
            valueData: this.processValue(result),
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
  }

  processValue(data) {
    this.valueChartPoints = [];
    var minDate;
    data.forEach((element) => {
      let point = {
        x: this.getDate(element['date']),
        y: element[this.state.field],
      };
      if (!minDate) {
        minDate = this.getDate(element['date']);
      }
      this.valueChartPoints.push(point);
    });
    this.setState({ minDate: minDate });
    this.rebuildChart();
  }

  getDate(dateString) {
    return moment(dateString);
  }

  rebuildChart() {
    let chartData = {
      labels: ['Scatter'],
      datasets: [this.buildSeries(this.state.field, this.valueChartPoints, 'rgba(0,192,0,0.4)', false, null)],
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
    var styleHeight;
    styleHeight = 'summary-chart';
    if (this.state.mobile === 'true') {
      styleHeight = 'summary-chart-mobile';
    }
    return (
      <div className={styleHeight}>
        <Scatter
          data={this.state}
          options={{
            maintainAspectRatio: false,
            title: {
              display: true,
              text: this.state.title,
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
                  return formatDate(t.xLabel) + ' : ' + Math.round(t.value * 100).toLocaleString() + '%';
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
                    min: this.state.minDate,
                    max: new Date(),
                  },
                },
              ],
              yAxes: [
                {
                  ticks: {
                    callback: function (value, index, values) {
                      return Math.round(value * 100).toLocaleString() + '%';
                    },
                  },
                },
              ],
            },
          }}
        />
      </div>
    );
  }
}

export default SummaryLinePercentage;
