import PieChart from '../widget_templates/PieChart.js';

class ExchangePie extends PieChart {
  calculateBackgroundColor(value, maxValue) {
    if (value < 0) {
      value = 0;
    }
    let r = Math.round((0 * (value * 1.0)) / maxValue);
    let g = Math.round((255 * (value * 1.0)) / maxValue);
    let b = Math.round((255 * (value * 1.0)) / maxValue);
    //return 'rgba(' + r + ',' + g + ',' + b + ',0.5)';
    return '#a66d2e55';
  }

  borderColor() {
    return '#a66d2e5ff';
  }

  title() {
    return 'Exchange';
  }

  buildSummarizedHoldings(holdings) {
    let map = {};
    holdings.forEach((element) => {
      let holding = element['exchange'];
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
        label: key,
        value: value['value'],
      };
      if (value['quantity'] > 0) {
        result.push(row);
        index++;
      }
    }
    result.sort((a, b) => (a.value > b.value ? 1 : -1));
    return result;
  }
}

export default ExchangePie;
