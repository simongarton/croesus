import React from 'react';
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
    };
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

  buildHoldingChart(element, index) {
    return <ValueLine key={index} exchange={element['exchange']} symbol={element['symbol']} />;
  }

  render() {
    const fields = [];
    let index = 0;
    if (this.state.response['holdings']) {
      this.state.response['holdings'].forEach((element) => {
        fields.push(this.buildHoldingChart(element, index));
        index++;
      });
    }

    return (
      <div>
        <TotalValue />
        <TotalValueColumn />
        <TotalValueLine />
        <GainLossLine />
        {fields}
      </div>
    );
  }
}
