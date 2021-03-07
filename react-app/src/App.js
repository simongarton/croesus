import React from 'react';
import TotalValueColumn from './charts/TotalValueColumn.js';
import TotalValueLine from './charts/TotalValueLine.js';

// https://www.educative.io/edpresso/how-to-use-chartjs-to-create-charts-in-react

export default class App extends React.Component {
  render() {
    return (
      <div>
        <TotalValueColumn/>
        <TotalValueLine/>
      </div>
    );
  }
}