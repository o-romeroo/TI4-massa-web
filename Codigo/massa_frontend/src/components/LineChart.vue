<template>
  <div style="position: relative;">
    <div class="controls">
      <v-col cols="auto">
        <v-btn density="default" icon="mdi-reload" @click="resetZoom" class="reload-button top-0 right-0"
          style="position: absolute;" variant="plain" />
      </v-col>
    </div>
    <canvas :id="chartId"></canvas>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import zoomPlugin, { resetZoom } from "chartjs-plugin-zoom";

export default {
  name: "LineChart",
  props: {
    xLabels: {
      type: Array,
      required: true,
    },
    yValues: {
      type: Array,
      required: true,
    },
    chartKey: {
      type: [String, Number],
      required: true,
    },
    title: {
      type: String,
      required: false,
      default: "teste",
    }
  },
  computed: {
    chartId() {
      return `lineChart-${this.chartKey}`;
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    Chart.register(zoomPlugin);

    const ctx = document.getElementById(this.chartId).getContext("2d");
    this.chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: this.xLabels,
        datasets: [
          {
            label: "Euclides Distance",
            data: this.yValues,
            borderColor: "black",
            backgroundColor: "black",
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Plot of Euclidean Distances from " + this.title + " HCA",
            font: {
              size: 20, 
              weight: 'bold', 
            }
          },
          legend: {
            display: false,
            labels: {
              color: "#333",
            },
          },
          zoom: {
            zoom: {
              wheel: {
                enabled: true,
              },
              pinch: {
                enabled: true,
              },
              mode: "x",
            },
            pan: {
              enabled: true,
              mode: "x",
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true
            },
          },
          y: {
            title: {
              display: true,
              text: "Euclidean distance",
            },
          },
        },
      },
    });

    this.resetZoom();
  },
  methods: {
    resetZoom() {
      this.chart.resetZoom();
    },
  }
};
</script>


<style scoped></style>