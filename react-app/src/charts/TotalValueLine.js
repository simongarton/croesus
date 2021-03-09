import React from 'react';
import {Scatter} from 'react-chartjs-2';
import moment from 'moment';

function formatDate(date) {
  const s = date.toLocaleString();
  const parts = s.split(',')
  return parts[0] + ',' + parts[1];
}

class TotalValueColumn extends React.Component {

    constructor(props) {
        super();
        this.state = {};
    }

    componentDidMount() {
        fetch("https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/history")
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
      let chartPoints = [];
      data.forEach(element => {
          let point = {
            'x':moment(element['date']),
            'y':element['value'],
          }
          chartPoints.push(point)
      });
      console.log(chartPoints)
      let chartData = {
        labels: ['Scatter'],
        datasets: [
          {
            label: 'Total Value',
            fill: false,
            backgroundColor: 'rgba(75,192,192,0.4)',
            pointBorderColor: 'rgba(75,192,192,1)',
            pointBackgroundColor: '#fff',
            pointBorderWidth: 5,
            pointHoverRadius: 10,
            pointHoverBackgroundColor: 'rgba(75,192,192,1)',
            pointHoverBorderColor: 'rgba(220,220,220,1)',
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            showLine: true,
            data: chartPoints
          }
        ]
      };
      this.setState(chartData);
    }

    render() {
        return <Scatter
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
          },
          tooltips: {
            mode: 'index',
            intersect: false,
            callbacks: {
                label: function (t, d) {
                  return formatDate(t.xLabel) + ' : $' + Math.round(t.value).toLocaleString();
                }
            }
        },
          scales: {
            xAxes: [{
                type: 'time',          
                time: {
                    unit: 'day'
                },
                ticks: {
                  min:'2020-01-01',
                  max:'2022-01-01'
              }

            }],
            yAxes: [{
              ticks: {
                  callback: function(value, index, values) {
                    //return value.toLocaleString("en-US",{style:"currency", currency:"USD"});
                    return '$' + Math.round(value).toLocaleString();
                  }
              }
          }]
        }
        }}
      />

    }
  }

export default TotalValueColumn;