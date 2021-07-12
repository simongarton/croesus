import React from 'react';
import { Card } from 'react-bootstrap';
import { Pie } from 'react-chartjs-2';

class PieChart extends React.Component {
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

  calculateBackgroundColor(value, maxValue) {
    return 'rgba(255,0,0,0.9)';
  }

  borderColor() {
    return 'rgba(255,0,0,0.9)';
  }

  title() {
    return 'Title';
  }

  getToolTipTitle(tooltipItem, data) {
    const value = data['labels'][tooltipItem[0]['index']];
    return value;
  }

  getToolTipValue(tooltipItem, data) {
    const value = data['datasets'][0]['data'][tooltipItem['index']];
    return '$' + Math.round(value).toLocaleString();
  }

  processData(data) {
    let holdings = data['holdings'] == null ? [] : this.buildSummarizedHoldings(data['holdings']);
    let chartPoints = [];
    let chartLabels = [];
    let backgroundColors = [];
    let maxValue = 0;
    holdings.forEach((element) => {
      maxValue = element['value'] > maxValue ? element['value'] : maxValue;
    });
    holdings.forEach((element) => {
      chartLabels.push(element['label']);
      chartPoints.push(element['value']);
      backgroundColors.push(this.calculateBackgroundColor(element['value'], maxValue));
    });
    let chartData = {};
    chartData['labels'] = chartLabels;
    let chartDatasets = {
      label: this.title(),
      backgroundColor: backgroundColors,
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
      all: 200,
      helen: 200,
      simon: 200,
      trust: 200,
    };
    let height = heightTable[this.state.account] ? heightTable[this.state.account] : 100;
    return (
      <Card className="mb-1">
        <Pie
          data={this.state}
          height={height}
          options={{
            title: {
              display: true,
              text: this.title(),
              fontSize: 20,
            },
            cutoutPercentage: 30,
            layout: {
              padding: {
                bottom: 20,
              },
            },
            legend: {
              display: false,
              position: 'right',
            },
            tooltips: {
              callbacks: {
                title: this.getToolTipTitle,
                label: this.getToolTipValue,
              },
            },
            scales: {},
          }}
        />
      </Card>
    );
  }
}

export default PieChart;
