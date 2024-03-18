<template>
  <div class="iphone-container">
    <!-- Your Home Page Content -->

    <div class="home-content">
      <!-- BANNER AT TOP -->
      <div class="top-banner">
        <!-- LINEAR BANNER ONLY-->
        <svg xmlns="http://www.w3.org/2000/svg" width="373" height="189" viewBox="0 0 373 189" fill="none">
          <path d="M0 167.65C0 167.65 35 189 187.5 189C340 189 375 167.65 375 167.65L374.937 0H0.0633623L0 167.65Z"
            fill="url(#paint0_linear_1_2516)" />
          <defs>
            <linearGradient id="paint0_linear_1_2516" x1="187.5" y1="189" x2="187.5" y2="0"
              gradientUnits="userSpaceOnUse">
              <stop stop-color="#E3652F" stop-opacity="0.77" />
              <stop offset="1" stop-color="#E3652F" stop-opacity="0" />
            </linearGradient>
          </defs>
        </svg>

        <!-- IMAGE BANNER OVERLAY -->
        <div class="banner-overlay">
          <img src="../assets/w4.png" alt="Banner Image">
          <div class="text-overlay">
            <br>
            <span class="usage-count">Currrent Usage</span>
            <br>
            <span class="usage-value"><span class="usage-value-number">250</span>W</span>
          </div>
        </div>
      </div>

      <!-- MAIN CONTENT -->
      <div class="bottom-banner">
        <!-- List of appliances -->
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)


export default defineComponent({
  name: 'BarChart',
  components: { Bar },
  data() {
    const today = new Date();
    const currentMonth = today.getMonth();
    const labels = [];

    // Generate labels for the past 6 months from the current month
    for (let i = 5; i >= 0; i--) {
      const monthIndex = (currentMonth - i + 12) % 12;
      labels.push(this.getMonthName(monthIndex));
    }

    return {
      chartData: {
        labels: labels,
        datasets: [
          {
            label: 'Electric',
            data: this.generateElectricityData(currentMonth),
            backgroundColor: 'rgba(227, 101, 47, 0.90)', // Red color for gas
            stack: 'stack1'
          },
          {
            label: 'Gas',
            data: this.generateGasData(currentMonth),
            backgroundColor: 'rgba(0, 69, 107, 0.90)', // Blue color for electricity
            stack: 'stack1'
          }
        ]
      },
      chartOptions: {
        responsive: true,
        scales: {
          x: {
            stacked: true,
            ticks: {
              color: 'rgba(227, 101, 47, 0.90)', // Set x-axis text color to black
              font: {
                weight: 'bold' // Set legend text font weight to bold
              }
            }
          },
          y: {
            stacked: true,
            ticks: {
              color: 'rgba(0, 69, 107, 0.90)',
              font: {
                weight: 'bold' // Set legend text font weight to bold
              } // Set x-axis text color to black
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || '';

                if (label) {
                  label += ': ';
                }

                if (context.parsed.y !== null) {
                  label += '£' + context.parsed.y.toFixed(2);
                }

                return label;
              }
            }
          },
          legend: {
            labels: {
              color: 'white', // Set legend text color to black
              font: {
                weight: 'bold' // Set legend text font weight to bold
              }
            }

          }
        }
      }
    }
  },
  methods: {
    getMonthName(monthIndex) {
      const monthNames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
      return monthNames[monthIndex];
    },
    generateGasData(currentMonth) {
  // Assumed gas usage data for each month (replace with real data)
  const gasUsage = [80, 75, 70, 85, 80, 75, 90, 85, 80, 75, 70, 85];
  return gasUsage.map(wattage => this.calculateCost(wattage)).map(cost => Math.floor(Math.random() * (300 - 100 + 1)) + 100); // Generate random cost within the range of 100 to 300
},
generateElectricityData(currentMonth) {
  // Assumed electricity usage data for each month (replace with real data)
  const electricityUsage = [200, 210, 220, 215, 205, 210, 200, 215, 220, 225, 230, 220];
  return electricityUsage.map(wattage => this.calculateCost(wattage)).map(cost => Math.floor(Math.random() * (300 - 100 + 1)) + 100); // Generate random cost within the range of 100 to 300
},
    calculateCost(wattage) {
      // Add your cost calculation logic here
      const cost = (wattage / 1000) * 1.5; // Assuming $1.5 per kWh

      // Round to two decimal places
      return Number(cost.toFixed(2));
    },
    checkAuthStatus() {
      fetch('/check_auth/')
        .then(response => response.json())
        .then(data => {
          if (!data.authenticated) {
            window.location.href = '/login/';
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    getApplianceWithMostUsage() {
      fetch('/get_appliance_with_most_usage/')
        .then(response => response.json())
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  },
  mounted() {
    this.checkAuthStatus();
  }
})
</script>

<style scoped>
.iphone-container {
  display: flex;
  justify-content: center;
  align-items: center;
  /* height: 100vh; Use full viewport height */
}

.iphone {
  width: 375px;
  /* iPhone X width */
  height: 812px;
  /* iPhone X height */
  background-color: #fff;
  border-radius: 39px;
  /* iPhone X border radius */
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.iphone-inner {
  width: calc(100% - 20px);
  height: calc(100% - 20px);
  border: 5px solid #ccc;
  /* Add inner border */
  border-radius: 29px;
  /* Adjust border-radius to match inner part */
  overflow: hidden;
  position: relative;
}

.iphone-bottom {
  display: flex;
  justify-content: space-around;
  align-items: center;
  position: absolute;
  bottom: 20px;
  width: calc(100% - 5px);
}


.iphone-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  outline: none;
}

.iphone-button img {
  width: 24px;
  height: 24px;
  margin-bottom: 4px;
}

.top-banner {
  position: relative;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.banner-overlay img {
  width: 50%;
  /* Adjust image size */
  height: 15%;
  /* Adjust image size */
}

.text-overlay {
  text-align: center;
  color: #fff;
  /* Adjust text color */
}

.usage-count {
  color: #FFF;
  font-size: 13px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}

.usage-value {
  color: #FFF;
  font-size: 20px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}

.usage-value-number {
  color: #FFF;
  font-size: 30px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}

.bottom-banner {
  margin-top: 15px;
  width: 375px;
  height: 596px;
  flex-shrink: 0;
  border-radius: 38px 38px 0px 0px;
  background: linear-gradient(180deg, rgba(227, 101, 47, 0.90) 0%, rgba(255, 255, 255, 0.00) 75%);
  box-shadow: 0px -15px 26px 0px rgba(0, 0, 0, 0.03);
}
</style>