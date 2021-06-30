import React from 'react';
import { Spinner } from 'react-bootstrap';

import SingleStat from '../components/SingleStat';

class TotalValueMobile extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
      account: props.account,
      small: props.small,
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
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/all_value';
    } else {
      url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value/' + account;
    }
    var t0 = performance.now();
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            response: result,
            isLoaded: true,
          });
          var t1 = performance.now();
          console.log('Call to ' + url + ' took ' + (t1 - t0) + ' milliseconds.');
        },
        (error) => {
          this.setState({
            response: null,
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

  buildRow(element, index) {
    let percentageLine;
    if (this.state.small && this.state.small === 'false') {
      percentageLine = (
        <td className={this.redGreen(element['percentage'], 'right-align table-cell-pad', 5)}>
          {this.formatPercentage(element['percentage'])}
        </td>
      );
    }

    return (
      <tr key={index}>
        <td className="left-align pad-right">{element['holding']}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className={this.redGreen(element['gain_loss'], 'right-align table-cell-pad', 2)}>{this.formatDollars(element['gain_loss'])}</td>
        {percentageLine}
        <td className={this.redGreen(element['weighted_cagr'], 'right-align table-cell-pad', 5)}>
          {this.formatPercentage(element['weighted_cagr'])}
        </td>
      </tr>
    );
  }

  removeNegativeZero(amount, n) {
    if (!amount) {
      return amount;
    }
    let amt = amount.toFixed(n);
    return amt;
  }

  redGreen(amount, otherStyles, n) {
    let amt = this.removeNegativeZero(amount, n);
    if (Number(amt) < 0) {
      return otherStyles + ' red-text';
    }
    if (Number(amt) >= 0) {
      return otherStyles + ' green-text';
    }
    return otherStyles;
  }

  formatDollars(amount) {
    let amt = this.removeNegativeZero(amount, 0);
    var formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'NZD', maximumFractionDigits: 0 });
    return formatter.format(amt);
  }

  formatNumber(amount) {
    var formatter = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2 });
    return formatter.format(amount);
  }

  formatPercentage(amount) {
    if (amount === null) {
      return amount;
    }
    let amt = (100 * amount).toFixed(4);
    return Number(amt).toLocaleString() + '%';
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
      result.push(this.buildRow(row, index));
      index++;
    }
    return result;
  }

  buildSingleStat(label, value, currency, percentage, redGreen) {
    return <SingleStat label={label} value={value} currency={currency} percentage={percentage} redGreen={redGreen} />;
  }

  render() {
    if (this.state.response == null) {
      return <Spinner animation="border" role="status"></Spinner>;
    }
    let totalValue = 0;
    let gainLoss = 0;
    let spend = 0;
    let percentage = 0;
    let cagr = 0;
    let fields = [];
    if (this.state.response['holdings']) {
      totalValue = this.state.response['total'];
      gainLoss = this.state.response['gain_loss'];
      spend = this.state.response['spend'];
      percentage = this.state.response['percentage'];
      cagr = this.state.response['cagr'];
      fields = this.buildSummarizedHoldings(this.state.response['holdings']);
    }

    let header;
    let percentageLine;
    if (this.state.small && this.state.small === 'false') {
      header = (
        <div className="mb-3 mt-3">
          <h3>Summary by stock</h3>
        </div>
      );
      percentageLine = <th className="right-align">%age</th>;
    } else {
      header = (
        <div>
          <h5>
            Total value ({this.state.account}): {this.formatDollars(totalValue)}
          </h5>
          {this.buildSingleStat('Value', totalValue, true, false)}
          {this.buildSingleStat('Spend', spend, true, false)}
          {this.buildSingleStat('Gain/Loss', gainLoss, true, false, true)}
          {this.buildSingleStat('Percentage', percentage, false, true, true)}
          {this.buildSingleStat('CAGR', cagr, false, true, true)}
        </div>
      );
    }
    return (
      <div className="pad-table code smaller-text">
        {header}
        <table className="margin-auto">
          <thead>
            <tr>
              <th className="left-align">holding</th>
              <th className="right-align">value</th>
              <th className="right-align">&nbsp;gain/loss</th>
              {percentageLine}
              <th className="right-align">cagr</th>
            </tr>
          </thead>
          <tbody>{fields}</tbody>
        </table>
      </div>
    );
  }
}

export default TotalValueMobile;
