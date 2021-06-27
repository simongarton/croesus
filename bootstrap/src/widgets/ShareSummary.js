import React from 'react';
import { Spinner } from 'react-bootstrap';

import SingleStat from '../components/SingleStat';

class ShareSummary extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
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

  buildSingleStat(label, value, currency, percentage, redGreen) {
    return <SingleStat label={label} value={value} currency={currency} percentage={percentage} redGreen={redGreen} />;
  }

  getSingleStat(label, key, currency, percentage) {
    return this.buildSingleStat(label, this.state.response[key], currency, percentage);
  }

  buildSharesForAccount(account) {
    const shareData = this.state.response;
    return (
      <div>
        <h1 className="code">{account}</h1>
        {this.buildSingleStat('Value', shareData['total'], true, false)}
        {this.buildSingleStat('Spend', shareData['spend'], true, false)}
        {this.buildSingleStat('Gain/Loss', shareData['gain_loss'], true, false, true)}
        {this.buildSingleStat('Percentage', shareData['percentage'], false, true, true)}
        {this.buildSingleStat('CAGR', shareData['cagr'], false, true, true)}
      </div>
    );
  }

  buildShares() {
    return this.buildSharesForAccount(this.state.account);
  }

  render() {
    if (this.state.response == null) {
      return (
        <div>
          <h1 className="code">{this.state.account}</h1>
          <Spinner animation="border" role="status"></Spinner>
        </div>
      );
    }
    return this.buildShares();
  }
}

export default ShareSummary;
