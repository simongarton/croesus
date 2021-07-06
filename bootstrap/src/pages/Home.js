import React from 'react';
import { Button, Spinner } from 'react-bootstrap';

import SingleStat from '../components/SingleStat';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      isUpdating: false,
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

  buildSingleCell(label, value, currency, percentage, redGreen) {
    return (
      <SingleStat label={label} value={value} currency={currency} percentage={percentage} redGreen={redGreen} key={label} cell={true} />
    );
  }

  getSingleStat(label, key, currency, percentage) {
    return this.buildSingleStat(label, this.state.response[key], currency, percentage);
  }

  buildSummary() {
    const valueFourPercent = this.state.response['total_value'] * 0.04; //'en-US', { style: 'currency', currency: 'USD' });
    const value2halfMill = this.state.response['total_value'] / 2500000;
    return (
      <div>
        {this.getSingleStat('Total shares', 'share_value', true, false, false)}
        {this.getSingleStat('Other assets', 'other_value', true, false, false)}
        {this.getSingleStat('Total value', 'total_value', true, false, false)}
        {this.buildSingleStat('4% value', valueFourPercent, true, false, false)}
        {this.buildSingleStat('2.5 million value', value2halfMill, false, true, false)}
      </div>
    );
  }

  buildSummaryAndOtherAssets() {
    const valueFourPercent = this.state.response['total_value'] * 0.04; //'en-US', { style: 'currency', currency: 'USD' });
    const value2halfMill = this.state.response['total_value'] / 2500000;
    const summary = (
      <div>
        {this.getSingleStat('Total shares', 'share_value', true, false, false)}
        {this.getSingleStat('Other assets', 'other_value', true, false, false)}
        {this.getSingleStat('Total value', 'total_value', true, false, false)}
        {this.buildSingleStat('4% value', valueFourPercent, true, false, false)}
        {this.buildSingleStat('2.5 million value', value2halfMill, false, true, false)}
      </div>
    );
    const assetLines = [];
    const otherAssets = this.state.response['other_data'];
    if (!otherAssets) {
      return <div>Ooops2</div>;
    }
    let otherAssetValue = 0;
    for (var i = 0; i < otherAssets.length; i++) {
      const otherAsset = otherAssets[i];
      otherAssetValue = otherAssetValue + otherAsset['value'];
      assetLines.push(
        this.buildSingleStat(otherAsset['asset'] + ' (' + otherAsset['account'] + ')', otherAsset['value'], true, false, false)
      );
    }
    assetLines.push(this.buildSingleStat('Total', otherAssetValue, true, false, false));
    return (
      <table className="margin-auto">
        <tr>
          <td>{summary}</td>
          <td className="table-spacer"></td>
          <td>{assetLines}</td>
        </tr>
      </table>
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

  getShareData(account, key, currency, percentage, redgreen) {
    if (!this.state.response['share_data']) {
      return <div>Oops</div>;
    }
    return this.buildSingleCell('', this.state.response['share_data'][account][key], currency, percentage, redgreen);
  }

  buildSharesTable() {
    return (
      <table className="code margin-auto">
        <tr>
          <td></td>
          <td>helen</td>
          <td>simon</td>
          <td>trust</td>
          <td>all</td>
        </tr>
        <tr>
          <td>Value</td>
          <td>{this.getShareData('helen', 'total', true, false, false)}</td>
          <td>{this.getShareData('simon', 'total', true, false, false)}</td>
          <td>{this.getShareData('trust', 'total', true, false, false)}</td>
          <td>{this.getShareData('all', 'total', true, false, false)}</td>
        </tr>
        <tr>
          <td>Spend</td>
          <td>{this.getShareData('helen', 'spend', true, false, false)}</td>
          <td>{this.getShareData('simon', 'spend', true, false, false)}</td>
          <td>{this.getShareData('trust', 'spend', true, false, false)}</td>
          <td>{this.getShareData('all', 'spend', true, false, false)}</td>
        </tr>
        <tr>
          <td>Gain/Loss</td>
          <td>{this.getShareData('helen', 'gain_loss', true, false, true)}</td>
          <td>{this.getShareData('simon', 'gain_loss', true, false, true)}</td>
          <td>{this.getShareData('trust', 'gain_loss', true, false, true)}</td>
          <td>{this.getShareData('all', 'gain_loss', true, false, true)}</td>
        </tr>
        <tr>
          <td>Percentage</td>
          <td>{this.getShareData('helen', 'percentage', false, true, true)}</td>
          <td>{this.getShareData('simon', 'percentage', false, true, true)}</td>
          <td>{this.getShareData('trust', 'percentage', false, true, true)}</td>
          <td>{this.getShareData('all', 'percentage', false, true, true)}</td>
        </tr>
        <tr>
          <td>CAGR</td>
          <td>{this.getShareData('helen', 'cagr', false, true, true)}</td>
          <td>{this.getShareData('simon', 'cagr', false, true, true)}</td>
          <td>{this.getShareData('trust', 'cagr', false, true, true)}</td>
          <td>{this.getShareData('all', 'cagr', false, true, true)}</td>
        </tr>
      </table>
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

  buildHomePageMobile() {
    let bottomSection = <div />;
    if (this.state.isUpdating) {
      bottomSection = <Spinner animation="border" role="status"></Spinner>;
    } else {
      bottomSection = (
        <Button variant="danger" onClick={this.recalculateValue.bind(this)}>
          Recalculate value
        </Button>
      );
    }
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
        <Button variant="danger" onClick={this.updateStuff.bind(this)}>
          Update cached data
        </Button>
        <div className="mb-2"></div>
        {bottomSection}
        <div className="mb-2"></div>
      </div>
    );
  }

  buildHomePageDesktop() {
    let bottomSection = <div />;
    if (this.state.isUpdating) {
      bottomSection = <Spinner animation="border" role="status"></Spinner>;
    } else {
      bottomSection = (
        <Button variant="danger" onClick={this.recalculateValue.bind(this)}>
          Recalculate value
        </Button>
      );
    }
    return (
      <div>
        <h1 className="code">Summary</h1>
        {this.buildSummaryAndOtherAssets()}
        <hr></hr>
        <h2 className="code">Shares</h2>
        {this.buildSharesTable()}
        <hr></hr>
        <p className="code text-muted smaller-text">updated at {this.buildUpdatedAt()}</p>
        <div className="mb-2"></div>
        <Button variant="danger" onClick={this.updateStuff.bind(this)}>
          Update cached data
        </Button>
        <div className="mb-2"></div>
        {bottomSection}
        <div className="mb-2"></div>
      </div>
    );
  }

  updateStuff() {
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/cache';
    fetch(url, { method: 'DELETE' })
      .then((res) => res.json())
      .then(
        (result) => {
          window.location.reload(false);
        },
        (error) => {
          console.log(error);
        }
      );
  }

  recalculateValue() {
    const url = 'https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value';
    this.setState({ isUpdating: true });
    fetch(url, { method: 'POST' })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState({ isUpdating: false });
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
    const mqlMobile = window.matchMedia('(max-width: 480px)');
    if (mqlMobile.matches) {
      return this.buildHomePageMobile();
    } else {
      return this.buildHomePageDesktop();
    }
  }
}

export default Home;
