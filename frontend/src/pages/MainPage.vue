<template>
  <div class="loading-overlay" v-if="isLoading">Logging out...
    <div class="loading-spinner"></div>
  </div>
  <div class="iphone-container">
    <div class="home-content">
      <div class="top-banner">
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
            <h5>£{{ (costPrice * 12).toFixed(0) }}</h5>
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
      gasTotalSum: 0,
      electricityTotalSum: 0,
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
            backgroundColor: 'rgba(227, 101, 47, 0.90)', 
            stack: 'stack1'
          },
          {
            label: 'Gas',
            data: this.generateGasData(currentMonth),
            backgroundColor: 'rgba(0, 69, 107, 0.90)', 
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
              color: 'rgba(227, 101, 47, 0.90)', 
              font: {
                weight: 'bold' 
              }
            }
          },
          y: {
            stacked: true,
            ticks: {
              color: 'rgba(0, 69, 107, 0.90)',
              font: {
                weight: 'bold' 
              }
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
              color: 'white', 
              font: {
                weight: 'bold' 
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
          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);
          const gasAppliances = this.appliancesList.filter((appliance: { type: string; wattage: any; }) => appliance.type === 'gas');
          const gasUsage = gasAppliances.map((appliance: { type: string; wattage: any; }) => appliance.wattage);
          const gasSum = gasUsage.reduce((total, wattage) => total + wattage, 0);
          const gasCost = this.calculateCost(gasSum);
          this.gasData = gasCost;
        })
        .catch(error => {
          console.error('Error:', error);
        });
        this.gasTotalSum = Math.random() * (95 - 40) + 40;
        const gasUsage = [];
        for (let i = 0; i < 12; i++) {
          const randomFactor = Math.random() * (1.09 - 0.97) + 0.97; 
          const randomUsage = this.gasTotalSum * randomFactor;
          gasUsage.push(randomUsage);
        }
        return gasUsage.map(wattage => this.calculateCost(wattage));
    },
    generateElectricityData() {
      fetch('/get_appliances/')
        .then(response => response.json())
        .then(data => {
          this.appliancesList = data.appliances;
          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);
          const electricityAppliances = this.appliancesList.filter((appliance: { type: string; wattage: any; }) => appliance.type === 'electricity');
          const electricityUsage = electricityAppliances.map((appliance: { type: string; wattage: any; }) => appliance.wattage);
          const electricSum = electricityUsage.reduce((total, wattage) => total + wattage, 0);
          const electricCost = this.calculateCost(electricSum);
          this.electricityData = electricCost;
        })
        .catch(error => {
          console.error('Error:', error);
        });

        this.electricityTotalSum = Math.random() * (300 - 150) + 150; 
        const electricityUsage = [];
        for (let i = 0; i < 12; i++) {
          const randomFactor = Math.random() * (1.20 - 0.875) + 0.875; 
          const randomUsage = this.electricityTotalSum * randomFactor; 
          electricityUsage.push(randomUsage);
        }
        return electricityUsage.map(wattage => this.calculateCost(wattage));
    },
    calculateCost(wattage: any) {
      const cost = wattage * 0.15; 

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

          this.appliancesList.sort((a: { wattage: any; }, b: { wattage: any; }) => b.wattage - a.wattage);

          this.mostUsedAppliance = (this.appliancesList[0] as { name: string }).name;

          this.energyUsage = this.appliancesList.reduce((total: any, appliance: { wattage: any; }) => total + appliance.wattage, 0);
          this.costPrice = Number(((this.energyUsage / 1000) * 1.5).toFixed(2));
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    logout() {
      this.showLoading();

      setTimeout(() => {

        this.hideLoading();
        window.location.href = '/login/';
      }, 3000);

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
}

.iphone {
  width: 375px;
  height: 812px;
  background-color: #fff;
  border-radius: 39px;
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
  border-radius: 29px;
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
  height: 15%;
}

.text-overlay {
  text-align: center;
  color: #fff;
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
  height: 50px;
  border-radius: 20px;
  background-color: rgba(227, 101, 47, 0.90);
  margin: 25px auto 0;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #FFF;
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
  color: #FFF;
}

.annualReview::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: rgba(0, 69, 107, 0.90);
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
  top: 34px;
  cursor: pointer;
  width: 30px;
  height: 30px;
  cursor: pointer;
  z-index: 100;
}

.loading-overlay {
  position: absolute;
  top: 27%;
  left: 0;
  width: 100%;
  height: 62%;
  border-radius: 38px 38px 38px 38px;
  color: white;
  background: linear-gradient(180deg, rgba(227, 101, 47, 1) 0%, rgb(65, 63, 63) 75%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #fff;
  border-radius: 50%;
  margin-left: 10px;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  z-index: 1001;
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