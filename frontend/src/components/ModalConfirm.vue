<template>
  <div class="absolute inset-0 overflow-y-auto bg-black bg-opacity-50">
    <div class="flex items-start justify-center min-h-screen mt-24 text-center">
      <div class="bg-white text-black rounded-lg text-center shadow-xl p-6 w-64" role="dialog" aria-modal="true">
        <h3>Add Appliance</h3>

        <div class="mt-4">
          <label for="applianceName">Name:</label>
          <input type="text" id="applianceName" v-model="newAppliance.name" class="border border-gray-400 p-2 w-full" />
        </div>

        <div class="mt-4">
          <label for="applianceWattage">Wattage:</label>
          <input type="number" id="applianceWattage" v-model="newAppliance.wattage"
            class="border border-gray-400 p-2 w-full" />
        </div>

        <div class="flex justify-center py-4 text-white">
          <button @click="addAppliance" class="border border-black bg-white text-black mr-4">
            Add
          </button>
          <button @click="$emit('close')">Cancel</button>
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


  defineEmits(['close']);

};
</script>
