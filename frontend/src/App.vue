<template>
    <div class="screen-container">
      <div class="iphone">
        <div class="iphone-inner">
          <div class="iphone-bottom">
            <router-link class="iphone-button" :to="{ name: 'Home' }">
              <i class="fa fa-home" aria-hidden="true"></i>
              Home
            </router-link>
            <router-link class="iphone-button" :to="{ name: 'Usage' }">
              <i class="fa fa-bar-chart"></i>
              Usage
            </router-link>
            <router-link class="iphone-button" :to="{ name: 'Advice' }">
              <i class="fa fa-lightbulb-o"></i>
              Advice
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";

export default defineComponent({
  components: { RouterLink },
});
</script>

<style scoped>
.screen-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* Use full viewport height */
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
</style>
