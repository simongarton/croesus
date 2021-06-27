import React from 'react';
import { Spinner } from 'react-bootstrap';

import SingleStat from '../components/SingleStat';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
    };
  }

  componentDidMount() {
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/summary';
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

  buildSingleStat(label, value, currency, percentage, redGreen) {
    return <SingleStat label={label} value={value} currency={currency} percentage={percentage} redGreen={redGreen} />;
  }

  getSingleStat(label, key, currency, percentage) {
    return this.buildSingleStat(label, this.state.response[key], currency, percentage);
  }

  buildSummary() {
    const valueFourPercent = this.state.response['total_value'] * 0.04; //'en-US', { style: 'currency', currency: 'USD' });
    return (
      <div>
        {this.getSingleStat('Total shares', 'share_value', true, false, false)}
        {this.getSingleStat('Other assets', 'other_value', true, false, false)}
        {this.getSingleStat('Total value', 'total_value', true, false, false)}
        {this.buildSingleStat('4% value', valueFourPercent, true, false, false)}
      </div>
    );
  }

  buildSharesForAccount(account) {
    const shareData = this.state.response['share_data'][account];
    return (
      <div>
        <h3 className="code">{account}</h3>
        {this.buildSingleStat('Value', shareData['total'], true, false)}
        {this.buildSingleStat('Spend', shareData['spend'], true, false)}
        {this.buildSingleStat('Gain/Loss', shareData['gain_loss'], true, false, true)}
        {this.buildSingleStat('Percentage', shareData['percentage'], false, true, true)}
        {this.buildSingleStat('CAGR', shareData['cagr'], false, true, true)}
      </div>
    );
  }

  buildShares() {
    return (
      <div>
        {this.buildSharesForAccount('all')}
        {this.buildSharesForAccount('helen')}
        {this.buildSharesForAccount('simon')}
        {this.buildSharesForAccount('trust')}
      </div>
    );
  }

  buildOtherAssets() {
    const assetLines = [];
    const otherAssets = this.state.response['other_data'];
    for (var i = 0; i < otherAssets.length; i++) {
      const otherAsset = otherAssets[i];
      assetLines.push(
        this.buildSingleStat(otherAsset['asset'] + ' (' + otherAsset['account'] + ')', otherAsset['value'], true, false, false)
      );
    }

    return <div>{assetLines}</div>;
  }

  buildHomePage() {
    return (
      <div>
        <h1 className="code">Summary</h1>
        {this.buildSummary()}
        <hr></hr>
        <h2 className="code">Shares</h2>
        {this.buildShares()}
        <hr></hr>
        <h2 className="code">Other assets</h2>
        {this.buildOtherAssets()}
        <hr></hr>
      </div>
    );
  }

  render() {
    if (this.state.response == null) {
      return (
        <div>
          <h1 className="code">Summary</h1>
          <Spinner animation="border" role="status"></Spinner>
        </div>
      );
    }
    return this.buildHomePage();
  }
}

export default Home;
