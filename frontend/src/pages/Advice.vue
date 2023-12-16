<template>
    <div class="screen-container">
      <div class="iphone">
        a
      </div>
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
      console.log("Assistance.vue");
      
      export default defineComponent({
          data() {
              return {
                  title: "Main Page",
              }
          }
      })
  </script>
  
  <style scoped>
  .screen-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* Use full viewport height */
  }
  
  .iphone {
    width: 375px; /* iPhone 6/7/8 width */
    height: 667px; /* iPhone 6/7/8 height */
    background-color: #fff;
    border-radius: 40px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    position: relative;
  }
  </style>
  