<template>
  <div class="loading-overlay" v-if="isLoading">Scanning for devices...
    <div class="loading-spinner"></div>
  </div>
  <div v-if="showInformationStep" class="absolute inset-0 overflow-y-auto bg-black bg-opacity-50 modalCSS">
    <div class="flex items-start justify-center min-h-screen mt-24 text-center">
      <div class="bg-custom-primary text-white rounded-lg text-center shadow-xl p-6 w-64" role="dialog"
        aria-modal="true">
        <h3 class="text-custom-heading">Step 1 / 2</h3>

        <div class="mt-4 infostepone">
          <span for="applianceName" class="text-custom-label">
            <p style="font-size: 20px; max-width: 350px; font-weight: 500">Please ensure WiFi is enabled on phone </p>
            <p style="font-size: 15px; font-weight: 500;">WattSmart will scan using WiFi to add all detected smart home
              devices</p>
          </span>
        </div>

        <div>
          Scanning might take few seconds
        </div>

        <div class="flex justify-center py-4 commandButtonsOne">
          <button @click="nextStep" class="bg-custom-button text-white px-4 py-2 rounded-md">
            Scan
          </button>
          <button @click="$emit('close')" class="text-custom-button px-4 py-2 rounded-md border border-custom-button">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="absolute inset-0 overflow-y-auto bg-black bg-opacity-50 modalCSS">
    <div class="flex items-start justify-center min-h-screen mt-24 text-center">
      <div class="bg-custom-primary text-white rounded-lg text-center shadow-xl p-6 w-64" role="dialog"
        aria-modal="true">
        <h3 class="text-custom-heading">Step 2 / 2</h3>

        <div class="mt-4 infostepone">
          <span for="applianceName" class="text-custom-label">
            <p style="font-size: 20px; max-width: 350px; font-weight: 500">Press button below to add all devices found
              on the current WiFi</p>
          </span>
        </div>

        <div class="flex justify-center py-4">
          <button @click="addAppliance" class="bg-custom-button text-white px-4 py-2 rounded-md">
            Add Devices
          </button>

        </div>
        <button @click="$emit('close')" class="text-custom-button px-4 py-2 rounded-md border border-custom-button"
          id="closeButton">
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Swal from 'sweetalert2'

const newAppliance = ref({
  name: '',
  type: '',
  wattage: 0,
});

const showInformationStep = ref(true);
const isLoading = ref(false);

const nextStep = () => {
  showLoading();
  setTimeout(() => {
    hideLoading();
    showInformationStep.value = false;
  }, 5000);
};

const showLoading = () => {
  isLoading.value = true;
};

const hideLoading = () => {
  isLoading.value = false;
};

const addAppliance = () => {
  const csrfToken = "{{ csrf_token }}";

  fetch('/add_appliance/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({
      name: newAppliance.value.name,
      type: newAppliance.value.type,
      wattage: newAppliance.value.wattage,
    })
  })
    .then(response => response.json())
    .then(data => {
      Swal.fire({
        position: "center",
        html: '<p>Appliances added successfully</p>',
        showConfirmButton: false,
        width: 300,
        timer: 1000
      });
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  var buttonToClose = document.getElementById('closeButton');

  buttonToClose?.click();

  window.location.href = '/';
};
</script>

<style scoped>
.modalCSS {
  padding-bottom: 100%;
  border-radius: 38px 38px 0px 0px;
  background: linear-gradient(180deg, rgba(227, 101, 47, 0.90) 0%, rgba(255, 255, 255, 0.00) 75%);
  box-shadow: 0px -15px 26px 0px rgba(0, 0, 0, 0.03);
}

.infostepone {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30%;
}

.commandButtonsOne {
  align-items: center;
  margin-top: 30%;

}

.bg-custom-primary {
  background-color: rgba(227, 101, 47, 0.90) 0%;
}

.text-custom-heading {
  color: #fff;
}

.text-custom-label {
  color: #fff;
}

.bg-custom-button {
  background-color: #E3652F;
  border: 1px solid #E3652F;
}

.border-custom-button {
  border-color: #E3652F;
  color: #E3652F;
}

.loading-overlay {
  position: absolute;
  top: 24%;
  left: 0;
  width: 100%;
  height: 67%;
  color: white;
  border-radius: 38px 38px 0px 0px;
  background: linear-gradient(180deg, rgba(227, 101, 47, 1) 0%, rgb(65, 63, 63) 75%);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #ffffff;
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

label {
  padding-right: 10px;
}
</style>
