import React from 'react';
import { Button, Spinner } from 'react-bootstrap';

import SingleStat from '../components/SingleStat';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: null,
    };
    this.updateStuff.bind(this);
  }

  componentDidMount() {
    this.getData();
  }

  getData() {
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/summary';
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
    return <SingleStat label={label} value={value} currency={currency} percentage={percentage} redGreen={redGreen} key={label} />;
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
    if (!this.state.response['share_data']) {
      return <div>Oops</div>;
    }
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

  buildUpdatedAt() {
    return this.state.response['updated_at'];
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
    if (!otherAssets) {
      return <div>Ooops2</div>;
    }
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
        <p className="code text-muted smaller-text">updated at {this.buildUpdatedAt()}</p>
        <div className="mb-2"></div>
        <Button variant="danger" onClick={this.updateStuff}>
          Update all data
        </Button>
        <div className="mb-2"></div>
      </div>
    );
  }

  updateStuff() {
    console.log(this);
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/cache';
    fetch(url, { method: 'DELETE' })
      .then((res) => res.json())
      .then(
        (result) => {
          console.log('deleted');
          window.location.reload(false);
        },
        (error) => {
          console.log(error);
        }
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
