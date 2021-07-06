import HorizontalBarChart from '../widget_templates/HorizontalBarChart.js';

class CAGRHorizontalBar extends HorizontalBarChart {
  backgroundColor() {
    return 'rgba(75,192,192,0.2)';
  }

  borderColor() {
    return 'rgba(75,192,192,0.9)';
  }

  title() {
    return 'CAGR';
  }

  labelFunction(t, d) {
    return Math.round(t.value).toLocaleString() + '%';
  }

  labelFunctionValues(value, index, values) {
    return Math.round(value).toLocaleString() + '%';
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
        label: key,
        value: (100 * value['weighted_cagr']) / value['value'],
      };
      if (value['quantity'] > 0) {
        result.push(row);
        index++;
      }
    }
    return result;
  }
}

export default CAGRHorizontalBar;
