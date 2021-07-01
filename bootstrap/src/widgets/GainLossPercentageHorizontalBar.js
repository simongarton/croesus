import HorizontalBarChart from './HorizontalBarChart.js';

class GainLossPercentageHorizontalBar extends HorizontalBarChart {
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
      chartPoints.push(element['percentage'] * 100);
    });
    let chartData = {};
    chartData['labels'] = chartLabels;
    let chartDatasets = {
      label: 'Value',
      backgroundColor: 'rgba(192,192,75,0.2)',
      borderColor: 'rgba(192,192,75,0.9)',
      borderWidth: 1,
      data: chartPoints,
    };
    chartData['datasets'] = [];
    chartData['datasets'].push(chartDatasets);
    this.setState(chartData);
  }
}

export default GainLossPercentageHorizontalBar;
