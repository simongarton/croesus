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
    fetch('https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value/' + account)
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
        <td className="left-align">{element['exchange'] + ':' + element['symbol']}</td>
        <td className="right-align table-cell-pad">{this.formatNumber(element['quantity'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['price'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['spend'])}</td>
        <td className={this.redGreen(element['gain_loss'], 'right-align table-cell-pad')}>{this.formatDollars(element['gain_loss'])}</td>
        <td className={this.redGreen(element['percentage'], 'right-align table-cell-pad')}>
          {this.formatPercentage(element['percentage'])}
        </td>
      </tr>
    );
  }

  redGreen(amount, otherStyles) {
    if (Number(amount) < 0) {
      return otherStyles + ' red-text';
    }
    if (Number(amount) > 0) {
      return otherStyles + ' green-text';
    }
    return otherStyles;
  }

  formatDollars(amount) {
    var formatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'NZD' });
    return formatter.format(amount);
  }

  formatNumber(amount) {
    var formatter = new Intl.NumberFormat('en-US', { minimumFractionDigits: 2 });
    return formatter.format(amount);
  }

  formatPercentage(amount) {
    return Number(amount).toLocaleString() + '%';
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
      <div className="pad-table">
        <h1>
          Total value ({this.state.account}): {this.formatDollars(totalValue)}
        </h1>
        <p>
          Spend : {this.formatDollars(spend)} &nbsp; Gain/Loss :{' '}
          <span className={this.redGreen(gainLoss)}>{this.formatDollars(gainLoss)} </span>&nbsp; {'% : '}
          <span className={this.redGreen(gainLoss)}>{this.formatPercentage(percentage)}</span>
        </p>
        <table>
          <thead>
            <tr>
              <th className="left-align">holding</th>
              <th className="right-align">quantity</th>
              <th className="right-align">price</th>
              <th className="right-align">value</th>
              <th className="right-align">spend</th>
              <th className="right-align">gain/loss</th>
              <th className="right-align">%</th>
            </tr>
          </thead>
          <tbody>{fields}</tbody>
        </table>
      </div>
    );
  }
}

export default TotalValue;
