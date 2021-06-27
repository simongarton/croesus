import React from 'react';

class TotalValueMobile extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
      account: props.account,
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
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({
            response: result,
            isLoaded: true,
          });
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
    return (
      <tr key={index}>
        <td className="left-align pad-right">{element['holding']}</td>{' '}
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className={this.redGreen(element['gain_loss'], 'right-align table-cell-pad', 2)}>{this.formatDollars(element['gain_loss'])}</td>
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
          weighted_cagr: element['cagr'] * element['quantity'],
        };
      } else {
        map[holding]['quantity'] = map[holding]['quantity'] + element['quantity'];
        map[holding]['value'] = map[holding]['value'] + element['value'];
        map[holding]['spend'] = map[holding]['spend'] + element['spend'];
        map[holding]['gain_loss'] = map[holding]['gain_loss'] + element['gain_loss'];
        map[holding]['weighted_cagr'] = map[holding]['weighted_cagr'] + element['cagr'] * element['quantity'];
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
        weighted_cagr: value['weighted_cagr'] / value['quantity'],
      };
      result.push(this.buildRow(row, index));
      index++;
    }
    return result;
  }

  render() {
    if (this.state.response == null) {
      return <h1>thinking ...</h1>;
    }
    let totalValue = 0;
    let gainLoss = 0;
    let spend = 0;
    let percentage = 0;
    let fields = [];
    if (this.state.response['holdings']) {
      totalValue = this.state.response['total'];
      gainLoss = this.state.response['gain_loss'];
      spend = this.state.response['spend'];
      percentage = this.state.response['percentage'];
      fields = this.buildSummarizedHoldings(this.state.response['holdings']);
      console.log('fields');
      console.log(fields);
    }

    return (
      <div className="pad-table code smaller-text">
        <h3>
          Total value ({this.state.account}): {this.formatDollars(totalValue)}
        </h3>
        <div>Spend : {this.formatDollars(spend)} </div>
        <div>
          Gain/Loss : <span className={this.redGreen(gainLoss, '', 2)}>{this.formatDollars(gainLoss)} </span>
        </div>
        <div>
          % : <span className={this.redGreen(gainLoss, '', 5)}>{this.formatPercentage(percentage)}</span>
        </div>
        <table>
          <thead>
            <tr>
              <th className="left-align">holding</th>
              <th className="right-align">value</th>
              <th className="right-align">&nbsp;gain/loss</th>
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
