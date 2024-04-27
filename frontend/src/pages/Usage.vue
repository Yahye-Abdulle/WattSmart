<script setup lang="ts">
import ModalConfirm from "../components/ModalConfirm.vue";
import { ref } from "vue";

const show = ref(false);

const openConfirm = () => {
    show.value = true;
};

const closeConfirm = () => {
    show.value = false;
};

</script>

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
                        <button class="add-appliance-button" @click="openConfirm">Add Appliance</button>
                    </div>
                </div>

            </div>
            <ModalConfirm v-if="show" @close="closeConfirm"></ModalConfirm>

            <!-- MAIN CONTENT -->
            <div class="bottom-banner">
                <div class="appliance-container">
                    <div class="appliance-list">
                        <div v-for="(appliance, index) in appliances" :key="index" class="appliance-item">
                            <div class="appliance-details">
                                <span class="appliance-name">{{ appliance.name }}</span>
                                <img src="https://cdn-icons-png.freepik.com/256/14025/14025835.png?semt=ais_hybrid"
                                    width="17" height="17" @click="deleteAppliance(appliance.name)"
                                    style="cursor: pointer;">
                                <span class="appliance-wattage">{{ appliance.wattage }}W / £{{
                            calculateCost(appliance.wattage) }}</span>
                                <div class="progress-bar-container">
                                    <div class="progress-bar"
                                        :style="{ width: calculateProgressBarWidth(appliance.wattage) }"></div>
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
import Swal from 'sweetalert2'

export default defineComponent({
    data() {
        return {
            title: "Home",
            appliances: [] as { name: string; wattage: number }[],
            csrfToken: '',
            totalWatts: 0,
        }
    },
    methods: {
        showAlert(message: string) {
            Swal.fire({
                position: "center",
                html: '<p>' + message + '</p>',
                showConfirmButton: false,
                width: 300,
                timer: 1000
            });
        },
        calculateCost(wattage: number) {
            const cost = wattage * 0.15;

            // Round to two decimal places
            return Number(cost.toFixed(2));
        },
        calculateProgressBarWidth(wattage: number) {
            return `${(wattage / this.totalWatts) * 100}%`; 
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
                    console.log('Success:', data);
                    this.appliances = data.appliances;

                    // Calculate total watts
                    this.totalWatts = this.appliances.reduce((total, appliance) => total + appliance.wattage, 0);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },
        deleteAppliance(name: string) {
            const csrfToken = "{{ csrf_token }}";

            fetch('/delete_appliance/' + name, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    name: name
                })
            })
                .then(response => response.json())
                .then(data => {
                    this.showAlert("Appliance Deleted Successfully!");
                    console.log('Success:', data);
                    this.getAppliance_USER();
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },
        getCookie(name: string) {
            // Function to get the value of a cookie by name
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts && parts.length === 2) return parts.pop()?.split(';').shift();
        },
    },
    mounted() {
        this.checkAuthStatus();
        this.getAppliance_USER();
        this.csrfToken = this.getCookie('csrftoken') ?? '';
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

.add-appliance-button {
    display: block;
    margin: 0 auto;
    margin-top: 25px;
    width: 200px;
    height: 50px;
    border-radius: 20px;
    background: #E3652F;
    ;
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
    max-height: 450px;
}

/* Hide scrollbar */
.appliance-container::-webkit-scrollbar {
    width: 0;
}

.appliance-list {
    margin-top: 25px;
}

.appliance-item {
    margin-bottom: 5px;
    color: #fff;
    padding-top: 3px;
}

.appliance-wattage {
    float: right;
    font-size: 13px;
    font-weight: 600;
    line-height: normal;
}
</style>