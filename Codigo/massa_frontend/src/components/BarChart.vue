<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'BarChart',
  props: {
    chartData: {
        title: "",
        labels: [],
        total: [],
        trainingSet: [],
        testSet: []
    }
  },
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      const ctx = this.$refs.chartCanvas.getContext('2d');

      const data = {
        labels: this.chartData.labels, 
        datasets: [
          {
            label: 'Total',
            data: this.chartData.total,
            backgroundColor: 'black',
            borderColor: 'black',
            borderWidth: 1
          },
          {
            label: 'Training set',
             data: this.chartData.training_set, 
            backgroundColor: 'gray',
            borderColor: 'gray',
            borderWidth: 1
          },
          {
            label: 'Test set',
             data: this.chartData.test_set, 
            backgroundColor: 'white',
            borderColor: 'black',
            borderWidth: 1
          }
        ]
      };


      const self = this; 

      const options = { 
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Frequency (%)'
            }
          }
        },
        plugins: {
          legend: {
            display: true,
            position: 'top',
            align: 'end'
          },
           title: {
             display: true,
             text: 'Distribution of datasets: ' + self.chartData.title,
             font: {
              size: 18, 
              weight: 'bold', 
            }
          }
        }
      };

      new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
      });
    }
  }
};
</script>