<template>
  <div v-if="showInformationStep" class="absolute inset-0 overflow-y-auto bg-black bg-opacity-50 modalCSS">
    <div class="flex items-start justify-center min-h-screen mt-24 text-center">
      <div class="bg-custom-primary text-white rounded-lg text-center shadow-xl p-6 w-64" role="dialog" aria-modal="true">
        <h3 class="text-custom-heading">Step 1 / 2</h3>

        <div class="mt-4 infostepone">
          <h3 for="applianceName" class="text-custom-label">Plug the appliance into the WattSmart socket</h3>
        </div>

        <div class="flex justify-center py-4 commandButtonsOne">
          <button @click="nextStep" class="bg-custom-button text-white px-4 py-2 rounded-md">
            Next
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
      <div class="bg-custom-primary text-white rounded-lg text-center shadow-xl p-6 w-64" role="dialog" aria-modal="true">
        <h3 class="text-custom-heading">Step 2 / 2</h3>

        <!-- Add Appliance Step -->
        <div class="mt-4">
          <label for="applianceWattage" class="text-custom-label">Give a name for appliance:</label>
          <input type="text" id="applianceName" v-model="newAppliance.name" class="border border-gray-400 p-2 w-full" placeholder="Name of appliance"/>
        </div>

        <div class="flex justify-center py-4">
          <button @click="addAppliance" class="bg-custom-button text-white px-4 py-2 rounded-md">
            Add
          </button>
          <button @click="$emit('close')" class="text-custom-button px-4 py-2 rounded-md border border-custom-button">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { defineEmits } from 'vue';

const newAppliance = ref({
  name: '',
  wattage: 0,
});

const showInformationStep = ref(true);

const nextStep = () => {
  showInformationStep.value = false;
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
      wattage: newAppliance.value.wattage,
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });

  // Emit the event to close the modal using the context.emit function
  defineEmits(['close']);
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

label {
  padding-right: 10px;
}
</style>
