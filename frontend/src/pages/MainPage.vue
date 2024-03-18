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
        <Bar
          id="my-chart-id"
          :options="chartOptions"
          :data="chartData"
        />
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
  const datasets = [{
    label: 'Average Watts Used',
    data: this.generateAverageWattsData(currentMonth),
    backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ],
    borderColor: 'rgba(54, 162, 235, 1)',
    borderWidth: 1
  }];

    // Generate labels for the past 6 months from March
    for (let i = 5; i >= 0; i--) {
      const monthIndex = (currentMonth - i + 12) % 12
      labels.push(this.getMonthName(monthIndex))
    }

    return {
      title: "Home",
      chartData: {
        labels: labels,
        datasets: datasets
      },
      chartOptions: {
        responsive: true
      }
    }
  },
  methods: {
    getMonthName(monthIndex) {
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return monthNames[monthIndex];
  },
  generateAverageWattsData(currentMonth) {
    // Assumed average watts data for each month (replace with real data)
    const averageWatts = [1200, 1100, 1000, 1050, 1250, 1300, 1400, 1350, 1100, 1000, 950, 1150];
    
    // Generate data for the past 6 months from the current month
    const data = [];
    for (let i = 5; i >= 0; i--) {
      const monthIndex = (currentMonth - i + 12) % 12;
      data.push(averageWatts[monthIndex]);
    }
    return data;
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