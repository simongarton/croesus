import React from 'react';
import { Button, Container, Row, Col, Card, Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class TotalValueMobileCard extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
    };
  }

  componentDidMount() {
    this.updateAmount();
  }

  updateAmount(account) {
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/all_value';
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

  buildRow(element, index) {
    return (
      <tr key={index}>
        <td className="left-align">{element['exchange'] + ':' + element['symbol']}</td>
        <td className="left-align">{element['account']}</td>
        <td className="right-align table-cell-pad">{this.formatNumber(element['quantity'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['price'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['value'])}</td>
        <td className="right-align table-cell-pad">{this.formatDollars(element['spend'])}</td>
        <td className={this.redGreen(element['gain_loss'], 'right-align table-cell-pad', 2)}>{this.formatDollars(element['gain_loss'])}</td>
        <td className={this.redGreen(element['percentage'], 'right-align table-cell-pad', 5)}>
          {this.formatPercentage(element['percentage'])}
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
    let amt = this.removeNegativeZero(amount, 2);
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

  getTable() {
    return (
      <table className="mobile-table-font mobile-table-pad">
        <thead>
          <tr>
            <th className="left-align">account</th>
            <th className="right-align">value</th>
            <th className="right-align">spend</th>
            <th className="right-align">gain/loss</th>
            <th className="right-align">%</th>
          </tr>
          <tr>
            <td className="left-align">total</td>
            <td className="right-align mobile-table-cell-pad">{this.formatDollars(this.state.response['total'])}</td>
            <td className="right-align mobile-table-cell-pad">{this.formatDollars(this.state.response['spend'])}</td>
            <td className={this.redGreen(this.state.response['gain_loss'], 'right-align mobile-table-cell-pad', 2)}>
              {this.formatDollars(this.state.response['gain_loss'])}
            </td>
            <td className={this.redGreen(this.state.response['gain_loss'], 'right-align mobile-table-cell-pad', 2)}>
              {this.formatPercentage(this.state.response['percentage'])}
            </td>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    );
  }

  render() {
    if (this.state.response == null) {
      return (
        <div>
          <Card>
            <Card.Title>Totals</Card.Title>
            <Card.Body className="text-muted">thinking</Card.Body>
          </Card>
        </div>
      );
    }
    console.log(this.state.response);

    return (
      <div>
        <Card>
          <Card.Title>Totals</Card.Title>
          <Card.Body>{this.getTable()}</Card.Body>
        </Card>
      </div>
    );
  }
}

export default TotalValueMobileCard;
