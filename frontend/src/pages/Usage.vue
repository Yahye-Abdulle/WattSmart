<template>
    <div class="iphone-container">
        <!-- Your Home Page Content -->

        <div class="home-content">
            <!-- BANNER AT TOP -->
            <div class="top-banner">
                <!-- LINEAR BANNER ONLY-->
                <svg xmlns="http://www.w3.org/2000/svg" width="373" height="189" viewBox="0 0 373 189" fill="none">
                    <path
                        d="M0 167.65C0 167.65 35 189 187.5 189C340 189 375 167.65 375 167.65L374.937 0H0.0633623L0 167.65Z"
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
                        <button class="add-appliance-button">Add Appliance</button>
                    </div>
                </div>
            </div>

            <!-- MAIN CONTENT -->
            <div class="bottom-banner">
                <!-- List of appliances -->
                <div class="appliance-container">
                    <div class="appliance-list">
                        <!-- Appliance 1 -->
                        <div class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">Microwave</span>
                                <span class="appliance-wattage">150W</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar" :style="{ width: '40%' }"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Appliance 2 -->
                        <div class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">Washing Machine</span>
                                <span class="appliance-wattage">100W</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar" :style="{ width: '20%' }"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Appliance 3 -->
                        <div class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">Dishwasher</span>
                                <span class="appliance-wattage">200W</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar" :style="{ width: '60%' }"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Appliance 4 -->
                        <div class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">TVs</span>
                                <span class="appliance-wattage">50W</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar" :style="{ width: '10%' }"></div>
                                </div>
                            </div>
                        </div>

                        <!-- Appliance 5 -->
                        <div class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">Dryer</span>
                                <span class="appliance-wattage">120W</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar" :style="{ width: '70%' }"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    data() {
        return {
            title: "Home",
        }
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

.add-appliance-button {
    /* Style the button center and smaller */
    display: block;
    margin: 0 auto;
    margin-top: 25px;
    width: 200px;
    height: 50px;
    border-radius: 20px;
    background: #E3652F;;
    color: #fff;
    font-size: 20px;
    font-weight: 600;
    border: none;
    outline: none;
    cursor: pointer;
    box-shadow: 0px -15px 26px 0px rgba(0, 0, 0, 0.03);
}

.progress-bar-container {
    height: 6px;
    background-color: #00456B;
    border-radius: 3px;
    margin-top: 5px;
}

.progress-bar {
    height: 100%;
    border-radius: 3px;
    background-color: #E3652F;
}

.appliance-container {
    max-width: 350px;
    margin-left: 10px;
    overflow-y: auto;
}

.appliance-list {
    margin-top: 25px;
}

.appliance-item {
    margin-bottom: 5px;
    color: #fff;
}

.appliance-wattage {
    /* Style the text next far right above progress bar */
    float: right;
    font-size: 13px;
    font-weight: 600;
    line-height: normal;
}
</style>