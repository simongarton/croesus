import React from 'react';
import {Bar} from 'react-chartjs-2';

class TotalValueColumn extends React.Component {

    constructor(props) {
        super();
        this.state = {};
    }

    componentDidMount() {
        //this.setState(this.loadData());
        fetch("https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/value")
            .then(res => res.json())
            .then(
                (result) => {
                this.setState({
                    isLoaded: true,
                    items: this.processData(result)
                });
                },
                // Note: it's important to handle errors here
                // instead of a catch() block so that we don't swallow
                // exceptions from actual bugs in components.
                (error) => {
                this.setState({
                    isLoaded: true,
                    error
                });
                }
            )
        }

    processData(data) {
        const holdings = data['holdings'];
        let chartPoints = [];
        let chartLabels = [];
        holdings.forEach(element => {
            chartLabels.push(element['exchange'] + '.' + element['symbol']);
            chartPoints.push(element['value'])
        });
        let chartData = {};
        chartData['labels'] = chartLabels;
        let chartDatasets = {
            label: 'Shares',
            backgroundColor: 'rgba(75,192,192,0.4)',
            borderColor: 'rgba(0,0,0,1)',
            borderWidth: 0,
            data: chartPoints
        }
        chartData['datasets'] = [];
        chartData['datasets'].push(chartDatasets);
        this.setState(chartData);
    }

    render() {
        return <Bar
        data={this.state}
        options={{
          title:{
            display:true,
            text:'Current value',
            fontSize:20
          },
          legend:{
            display:false,
            position:'right'
          }
        }}
      />

    }
  }

export default TotalValueColumn;