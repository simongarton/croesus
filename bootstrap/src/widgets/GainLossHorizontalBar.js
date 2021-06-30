import React from 'react';
import { HorizontalBar } from 'react-chartjs-2';

class GainLossHorizontalBar extends React.Component {
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
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
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
    let map = {};
    holdings.forEach((element) => {
      let holding = element['exchange'] + ':' + element['symbol'];
      if (!map[holding]) {
        map[holding] = {
          holding,
          quantity: element['quantity'],
          price: element['price'],
          value: element['value'],
          spend: element['spend'],
          gain_loss: element['gain_loss'],
          weighted_cagr: element['cagr'] * element['value'],
        };
      } else {
        map[holding]['quantity'] = map[holding]['quantity'] + element['quantity'];
        map[holding]['value'] = map[holding]['value'] + element['value'];
        map[holding]['spend'] = map[holding]['spend'] + element['spend'];
        map[holding]['gain_loss'] = map[holding]['gain_loss'] + element['gain_loss'];
        map[holding]['weighted_cagr'] = map[holding]['weighted_cagr'] + element['cagr'] * element['value'];
      }
    });
    const result = [];
    let index = 0;
    for (const [key, value] of Object.entries(map)) {
      let row = {
        index: index,
        holding: key,
        quantity: value['quantity'],
        value: value['value'],
        spend: value['spend'],
        gain_loss: value['gain_loss'],
        percentage: value['gain_loss'] / value['spend'],
        weighted_cagr: value['weighted_cagr'] / value['value'],
      };
      result.push(row);
      index++;
    }
    return result;
  }

  processData(data) {
    let holdings = data['holdings'] == null ? [] : this.buildSummarizedHoldings(data['holdings']);
    let chartPoints = [];
    let chartLabels = [];
    holdings.forEach((element) => {
      chartLabels.push(element['holding']);
      chartPoints.push(element['gain_loss']);
    });
    let chartData = {};
    chartData['labels'] = chartLabels;
    let chartDatasets = {
      label: 'Value',
      backgroundColor: 'rgba(192,75,192,0.2)',
      borderColor: 'rgba(192,75,192,0.9)',
      borderWidth: 1,
      data: chartPoints,
    };
    chartData['datasets'] = [];
    chartData['datasets'].push(chartDatasets);
    this.setState(chartData);
    console.log(chartData['labels'].length);
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
            text: 'Gain/Loss',
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
                return '$' + Math.round(t.value).toLocaleString();
              },
            },
          },
          scales: {
            xAxes: [
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

export default GainLossHorizontalBar;
