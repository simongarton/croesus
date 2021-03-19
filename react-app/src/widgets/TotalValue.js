import React from 'react';

class TotalValue extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
    };
    this.valueChartPoints = [];
    this.spendingChartPoints = [];
  }

  componentDidMount() {
    fetch('https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value')
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

  buildRow(element, index) {
    return (
      <tr key={index}>
        <td className="left-align">{element['exchange'] + ':' + element['symbol']}</td>
        <td className="right-align table-cell-pad">{this.formatNumber(element['quantity'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['price'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['spend'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['gain_loss'])}</td>
        <td className="right-align table-cell-pad">{this.formatPercentage(element['percentage'])}</td>
      </tr>
    );
  }

  formatDollars(amount) {
    return '$' + Number(amount).toLocaleString();
  }

  formatNumber(amount) {
    return Number(amount).toLocaleString();
  }

  formatPercentage(amount) {
    return Number(amount).toLocaleString() + '%';
  }

  render() {
    if (this.state.response == null) {
      return <h1>thinking ...</h1>;
    }
    const totalValue = this.state.response['total'];
    const gainLoss = this.state.response['gain_loss'];
    const spend = this.state.response['spend'];
    const percentage = this.state.response['percentage'];
    const fields = [];
    let index = 0;
    this.state.response['holdings'].forEach((element) => {
      fields.push(this.buildRow(element, index));
      index++;
    });

    console.log(this.state.response['holdings']);
    return (
      <div>
        <h1>Total value : {this.formatDollars(totalValue)}</h1>
        <p>
          Spend : {this.formatDollars(spend)} &nbsp; Gain/Loss : {this.formatDollars(gainLoss)} &nbsp; {'% : '}
          {this.formatPercentage(percentage)}
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
