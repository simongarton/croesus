import React from 'react';

class TotalValue extends React.Component {
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
        <td className="left-align pad-right">{element['exchange'] + ':' + element['symbol']}</td>
        <td className="left-align pad-right">{element['date']}</td>
        <td className="left-align ">{element['account']}</td>
        <td className="right-align table-cell-pad">{this.formatNumber(element['quantity'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['price'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['spend'])}</td>
        <td className={this.redGreen(element['gain_loss'], 'right-align table-cell-pad', 2)}>{this.formatDollars(element['gain_loss'])}</td>
        <td className={this.redGreen(element['percentage'], 'right-align table-cell-pad', 5)}>
          {this.formatPercentage(element['percentage'])}
        </td>
        <td className={this.redGreen(element['cagr'], 'right-align table-cell-pad', 5)}>{this.formatPercentage(element['cagr'])}</td>
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
    let amt = this.removeNegativeZero(amount, 2);
    var formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'NZD' });
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

  render() {
    if (this.state.response == null) {
      return <h1>thinking ...</h1>;
    }
    let totalValue = 0;
    let gainLoss = 0;
    let spend = 0;
    let percentage = 0;
    const fields = [];
    let index = 0;
    if (this.state.response['holdings']) {
      totalValue = this.state.response['total'];
      gainLoss = this.state.response['gain_loss'];
      spend = this.state.response['spend'];
      percentage = this.state.response['percentage'];
      this.state.response['holdings'].forEach((element) => {
        fields.push(this.buildRow(element, index));
        index++;
      });
    }

    return (
      <div className="pad-table code small-text">
        <h3>
          Total value ({this.state.account}): {this.formatDollars(totalValue)}
        </h3>
        <p>
          Spend : {this.formatDollars(spend)} &nbsp; Gain/Loss :{' '}
          <span className={this.redGreen(gainLoss, '', 2)}>{this.formatDollars(gainLoss)} </span>&nbsp; {'% : '}
          <span className={this.redGreen(gainLoss, '', 5)}>{this.formatPercentage(percentage)}</span>
        </p>
        <table>
          <thead>
            <tr>
              <th className="left-align">holding</th>
              <th className="left-align">date</th>
              <th className="left-align">account</th>
              <th className="right-align">quantity</th>
              <th className="right-align">price</th>
              <th className="right-align">value</th>
              <th className="right-align">spend</th>
              <th className="right-align">gain/loss</th>
              <th className="right-align">%</th>
              <th className="right-align">cagr</th>
            </tr>
          </thead>
          <tbody>{fields}</tbody>
        </table>
      </div>
    );
  }
}

export default TotalValue;
