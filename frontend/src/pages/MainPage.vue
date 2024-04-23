<template>
  <div class="loading-overlay" v-if="isLoading">Logging out...
    <div class="loading-spinner"></div>
  </div>
  <div class="iphone-container">
    <div class="home-content">
      <div class="top-banner">
        <!-- Logout Button Added -->
        <img src="../assets/logout.png" alt="Logout Image" @click="logout" class="logout-button">

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

        <div class="banner-overlay">
          <img src="../assets/w4.png" alt="Banner Image">
          <div class="text-overlay">
            <br>
            <span class="usage-count">Current Usage</span>
            <br>
            <span class="usage-value"><span class="usage-value-number">{{ Number((energyUsage * 0.178546).toFixed(0)) }}</span>W | £{{ costPrice
              }}</span>
          </div>
        </div>
      </div>

      <div class="bottom-banner">
        <h5 class="last6">LAST 6 MONTHS</h5>
        <Bar id="my-chart-id" :options="chartOptions" :data="chartData" />
        <div>
          <div class="applianceMostUsage">Most Used Appliance: {{ mostUsedAppliance }}</div>
        </div>

        <div class="annualReview">
          <div class="top-left">
            <p>Annual Spend</p>
            <h5>£{{ costPrice * 12 }}</h5>
          </div>
          <div class="top-right">
            <p>Annual Usage</p>
            <h5>{{ energyUsage }}W</h5>
          </div>
          <div class="bottom-left">
            <p>Electricity</p>
            <h5>£{{ electricityData }}</h5>
          </div>
          <div class="bottom-right">
            <p>Gas</p>
            <h5>£{{ gasData }}</h5>
          </div>
        </div>
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
    for (let i = 6; i >= 1; i--) {
      const monthIndex = (currentMonth - i + 12) % 12;
      labels.push(this.getMonthName(monthIndex));
    }

    return {
      isLoading: false,
      energyUsage: 0,
      costPrice: 0,
      mostUsedAppliance: '',
      annualReviewData: {
        electricity: 0,
        gas: 0,
        annualCost: 0
      },
      appliancesList: [],
      electricityData: 0,
      gasData: 0,
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
              label: function (context: { dataset: { label: string; }; parsed: { y: number | null; }; }) {
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
    getMonthName(monthIndex: any) {
      const monthNames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
      return monthNames[monthIndex];
    },
    generateGasData() {
      fetch('/get_appliances/')
        .then(response => response.json())
        .then(data => {
          this.appliancesList = data.appliances;

          // set appliance with most usage to mostUsedAppliance, straight here, no method needed
          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);

          // Get gas appliances from appliancesList
          const gasAppliances = this.appliancesList.filter((appliance: { type: string; wattage: any; }) => appliance.type === 'gas');

          // Extract wattages from gas appliances
          const gasUsage = gasAppliances.map((appliance: { type: string; wattage: any; }) => appliance.wattage);

          // Calculate total gas usage
          const gasSum = gasUsage.reduce((total, wattage) => total + wattage, 0);

          // Calculate gas cost
          const gasCost = this.calculateCost(gasSum);

          // Set gasData
          this.gasData = gasCost;

          // Return gas cost array
          return gasCost;

        })
        .catch(error => {
          console.error('Error:', error);
        });

    },
    generateElectricityData() {
      fetch('/get_appliances/')
        .then(response => response.json())
        .then(data => {
          this.appliancesList = data.appliances;

          // set appliance with most usage to mostUsedAppliance, straight here, no method needed
          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);

          // Get electricity appliances from appliancesList
          const electricityAppliances = this.appliancesList.filter((appliance: { type: string; wattage: any; }) => appliance.type === 'electricity');

          // Extract wattages from electricity appliances
          const electricityUsage = electricityAppliances.map((appliance: { type: string; wattage: any; }) => appliance.wattage);

          // Calculate total electricity usage
          const electricSum = electricityUsage.reduce((total, wattage) => total + wattage, 0);

          // Calculate electricity cost
          const electricCost = this.calculateCost(electricSum);

          // Set electricityData
          this.electricityData = electricCost;

          // Return electricity cost array
          return electricCost;

        })
        .catch(error => {
          console.error('Error:', error);
        });

    },
    calculateCost(wattage: any) {
      // Add your cost calculation logic here
      const cost = wattage * 0.15; // Assuming $1.5 per kWh

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
    getAppliance_USER() {
      fetch('/get_appliances/')
        .then(response => response.json())
        .then(data => {
          this.appliancesList = data.appliances;

          // set appliance with most usage to mostUsedAppliance, straight here, no method needed
          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);

          // Set the mostUsedAppliance to the first element (index 0) of the sorted array
          this.mostUsedAppliance = (this.appliancesList[0] as { name: string }).name;

          this.energyUsage = this.appliancesList.reduce((total: any, appliance: { wattage: any; }) => total + appliance.wattage, 0);
          this.costPrice = Number(((this.energyUsage / 1000) * 1.5).toFixed(2));

          // let eArray: number[] = [];
          // let gArray: number[] = [];

          // this.appliancesList.forEach((appliance: { type: string; wattage: any; }) => {
          //   // Check the type of the appliance
          //   if (appliance.type === 'electricity') {
          //     // If it's electricity, add its wattage to electricityData
          //     eArray.push(appliance.wattage);
          //   } else if (appliance.type === 'gas') {
          //     // If it's gas, add its wattage to gasData
          //     gArray.push(appliance.wattage);
          //   }
          // });


          // this.electricityData = this.calculateCost(eArray.reduce((total, wattage) => total + wattage, 0));
          // this.gasData = this.calculateCost(gArray.reduce((total, wattage) => total + wattage, 0));

        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    logout() {
      this.showLoading();

      setTimeout(() => {
        // Perform logout action here

        // After logout is complete, hide loading screen
        this.hideLoading();
        window.location.href = '/login/';
      }, 2000);

    },
    showLoading() {
      this.isLoading = true;
    },
    hideLoading() {
      this.isLoading = false;
    }
  },
  mounted() {
    this.checkAuthStatus();
    this.getAppliance_USER();
    this.generateElectricityData();
    this.generateGasData();
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

.last6 {
  color: #FFF;
  font-size: 20px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  margin-top: 20px;
  margin-left: 20px;
  text-align: center;
}

.applianceMostUsage {
  width: calc(100% - 5%);
  /* Adjust width as needed */
  height: 50px;
  /* Adjust height as needed */
  border-radius: 20px;
  background-color: rgba(227, 101, 47, 0.90);
  /* Background color */
  margin: 25px auto 0;
  /* Center horizontally and set top margin */
  display: flex;
  justify-content: center;
  align-items: center;
  color: #FFF;
  /* Text color */
  font-weight: bold;
}


.annualReview {
  width: calc(100% - 5%);
  height: 170px;
  background-color: rgba(227, 101, 47, 0.90);
  border-radius: 20px;
  margin: 10px auto;
  padding-left: 10px;
  padding-top: 5px;
  display: grid;
  grid-template-areas:
    "tl tr"
    "bl br";
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  position: relative;
  /* Add relative positioning */
  color: #FFF;
}

.annualReview::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  /* Adjust the height as needed */
  background-color: rgba(0, 69, 107, 0.90);
  /* Adjust the line color as needed */
}

.top-left {
  grid-area: tl;
}

.top-right {
  grid-area: tr;
}

.bottom-left {
  grid-area: bl;
}

.bottom-right {
  grid-area: br;
}

.logout-button {
  position: absolute;
  right: 10px;
  /* Adjusts the distance from the right edge */
  top: 34px;
  /* Adjusts the distance from the top edge */
  cursor: pointer;
  /* Changes the cursor to a pointer when hovering over the image */
  width: 30px;
  /* Adjust the width as necessary */
  height: 30px;
  /* Adjust the height as necessary */
  cursor: pointer;
  /* Ensures the cursor changes to a pointer when hovering the image */
  z-index: 100;
  /* Ensure it's on top if other elements are interfering */
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 88%;
  background-color: rgba(255, 255, 255, 0.8);
  /* Semi-transparent white background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* Ensure it's on top of other elements */
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  /* Light border color */
  border-top: 4px solid #333;
  /* Dark border color for spinner */
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  /* Animation for spinner rotation */
  z-index: 1001;
  /* Ensure it's on top of other elements */
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>: { dataset: { label: string; }; parsed: { y: number | null; }; }: string | number: number: { dataset: { label:
string; }; parsed: { y: number | null; }; }: string | number: number