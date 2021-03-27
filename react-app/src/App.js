import React from 'react';
import Button from '@material-ui/core/Button';

import TotalValueColumn from './charts/TotalValueColumn.js';
import TotalValueLine from './charts/TotalValueLine.js';
import GainLossLine from './charts/GainLossLine.js';
import TotalValue from './widgets/TotalValue.js';
import ValueLine from './charts/ValueLine.js';

// https://www.educative.io/edpresso/how-to-use-chartjs-to-create-charts-in-react

export default class App extends React.Component {
  constructor(props) {
    super();
    this.state = {
      isLoaded: false,
      response: {},
      account: 'all',
    };
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

  buildHoldingChart(element, index, account) {
    return <ValueLine key={index} account={account} exchange={element['exchange']} symbol={element['symbol']} />;
  }

  render() {
    const fields = [];
    let index = 0;
    let details = <div />;
    if (this.state.response['holdings']) {
      details = (
        <div>
          <TotalValueColumn account={this.state.account} />
          <TotalValueLine account={this.state.account} />
          <GainLossLine account={this.state.account} />
        </div>
      );
      this.state.response['holdings'].forEach((element) => {
        fields.push(this.buildHoldingChart(element, index, this.state.account));
        index++;
      });
    }

    return (
      <div>
        <Button
          onClick={() => {
            this.setState({ account: 'all' });
            this.updateAmount('all');
          }}
        >
          All
        </Button>
        <Button
          onClick={() => {
            this.setState({ account: 'simon' });
            this.updateAmount('simon');
          }}
        >
          Simon
        </Button>
        <Button
          onClick={() => {
            this.setState({ account: 'helen' });
            this.updateAmount('helen');
          }}
        >
          Helen
        </Button>
        <Button
          onClick={() => {
            this.setState({ account: 'trust' });
            this.updateAmount('trust');
          }}
        >
          Trust
        </Button>
        <TotalValue account={this.state.account} />
        {details}
        {fields}
      </div>
    );
  }
}
