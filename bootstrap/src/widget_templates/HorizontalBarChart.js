import React from 'react';
import { HorizontalBar } from 'react-chartjs-2';

class HorizontalBarChart extends React.Component {
  constructor(props) {
    super();
    this.state = {
      account: props.account,
    };
  }

  componentDidMount() {
    this.updateAmount(this.state.account);
  }

  updateAmount(account) {
    var url;
    if (account === 'all') {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/all_value';
    } else {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value/' + account;
    }
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: this.processData(result),
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
    this.setState({ account: nextProps.account });
    this.updateAmount(nextProps.account);
  }

  buildSummarizedHoldings(holdings) {
    return [];
  }

  backgroundColor() {
    return 'rgba(75,192,192,0.2)';
  }

  borderColor() {
    return 'rgba(75,192,192,0.9)';
  }

  title() {
    return 'Title';
  }

  labelFunction(t, d) {
    return Math.round(t.value).toLocaleString() + '%';
  }

  labelFunctionValues(value, index, values) {
    return Math.round(value).toLocaleString() + '%';
  }

  processData(data) {
    let holdings = data['holdings'] == null ? [] : this.buildSummarizedHoldings(data['holdings']);
    let chartPoints = [];
    let chartLabels = [];
    holdings.forEach((element) => {
      chartLabels.push(element['label']);
      chartPoints.push(element['value']);
    });
    let chartData = {};
    chartData['labels'] = chartLabels;
    let chartDatasets = {
      label: this.title(),
      backgroundColor: this.backgroundColor(),
      borderColor: this.borderColor(),
      borderWidth: 1,
      data: chartPoints,
    };
    chartData['datasets'] = [];
    chartData['datasets'].push(chartDatasets);
    this.setState(chartData);
  }

  render() {
    let heightTable = {
      all: 448,
      helen: 120,
      simon: 400,
      trust: 110,
    };
    let height = heightTable[this.state.account] ? heightTable[this.state.account] : 100;
    return (
      <HorizontalBar
        data={this.state}
        height={height}
        options={{
          title: {
            display: true,
            text: this.title(),
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
              label: this.labelFunction,
            },
          },
          scales: {
            xAxes: [
              {
                ticks: {
                  callback: this.labelFunctionValues,
                },
              },
            ],
          },
        }}
      />
    );
  }
}

export default HorizontalBarChart;
